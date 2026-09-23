"""Capteur différé : attendre qu'un fichier soit publié à une URL.

Pourquoi ne pas utiliser HttpSensor(deferrable=True) ?
Son déclencheur ne se remet en attente que sur une réponse 404. La source TLC
(CloudFront) répond 403 tant qu'un mois n'est pas publié : le déclencheur
boucle alors sans pause et bombarde le serveur. On écrit donc le nôtre.

Un capteur différé est fait de deux morceaux :
- l'OPÉRATEUR (FichierPublieSensor) tourne sur l'exécuteur. Il vérifie une
  fois, puis « se diffère » : il rend sa place et confie l'attente au
- DÉCLENCHEUR (FichierPublieTrigger), une coroutine asyncio qui tourne dans le
  service airflow-triggerer. Un seul triggerer fait patienter des centaines
  d'attentes à la fois sans occuper d'emplacement d'exécution.
Quand le déclencheur émet un événement, la tâche reprend dans execute_complete.
"""

from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import Any, AsyncIterator

import aiohttp
import requests
from airflow.sdk import BaseSensorOperator
from airflow.triggers.base import BaseTrigger, TriggerEvent

# Codes qui veulent dire « pas encore publié » : on attend, on n'échoue pas.
CODES_ABSENT = (403, 404)


def _lire_entetes(reponse_headers) -> dict[str, Any]:
    return {
        "taille": int(reponse_headers.get("Content-Length", 0)),
        "etag": reponse_headers.get("ETag", "").strip('"'),
        "modifie_le": reponse_headers.get("Last-Modified"),
    }


class FichierPublieTrigger(BaseTrigger):
    """Interroge l'URL (requête HEAD) toutes les `intervalle` secondes."""

    def __init__(self, url: str, intervalle: float = 3600):
        super().__init__()
        self.url = url
        self.intervalle = intervalle

    def serialize(self) -> tuple[str, dict[str, Any]]:
        # Le triggerer recrée l'objet à partir de ce chemin d'import et de ces arguments.
        return ("tlc.capteurs.FichierPublieTrigger", {"url": self.url, "intervalle": self.intervalle})

    async def run(self) -> AsyncIterator[TriggerEvent]:
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.head(self.url, timeout=aiohttp.ClientTimeout(total=30)) as rep:
                        if rep.status == 200:
                            yield TriggerEvent({"statut": "publie", "url": self.url, **_lire_entetes(rep.headers)})
                            return
                        if rep.status not in CODES_ABSENT:
                            yield TriggerEvent({"statut": "erreur", "url": self.url, "code": rep.status})
                            return
                        self.log.info("%s : pas encore publié (HTTP %s)", self.url, rep.status)
                except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
                    # Coupure réseau passagère : on réessaiera au prochain tour.
                    self.log.warning("%s : erreur réseau (%s)", self.url, exc)
                await asyncio.sleep(self.intervalle)


class FichierPublieSensor(BaseSensorOperator):
    """Attend la publication d'un fichier, sans occuper d'emplacement d'exécution.

    Renvoie (XCom) : {"statut", "url", "taille", "etag", "modifie_le"}.
    """

    template_fields = ("url",)

    def __init__(self, *, url: str, intervalle: float = 3600, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.intervalle = intervalle

    def execute(self, context):
        # Premier essai immédiat : si le fichier est déjà là, inutile de différer.
        rep = requests.head(self.url, timeout=30)
        if rep.status_code == 200:
            return {"statut": "publie", "url": self.url, **_lire_entetes(rep.headers)}
        if rep.status_code not in CODES_ABSENT:
            raise RuntimeError(f"{self.url} : réponse inattendue HTTP {rep.status_code}")
        self.log.info("Pas encore publié (HTTP %s) : attente confiée au triggerer.", rep.status_code)
        self.defer(
            trigger=FichierPublieTrigger(url=self.url, intervalle=self.intervalle),
            method_name="execute_complete",
            timeout=timedelta(seconds=self.timeout),
        )

    def execute_complete(self, context, event: dict[str, Any]):
        if event["statut"] != "publie":
            raise RuntimeError(f"{event['url']} : réponse inattendue HTTP {event.get('code')}")
        self.log.info("Publié : %s (%s octets)", event["url"], event["taille"])
        return event
