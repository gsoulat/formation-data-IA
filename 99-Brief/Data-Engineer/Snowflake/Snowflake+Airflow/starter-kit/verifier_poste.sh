#!/usr/bin/env bash
# Vérifie que le poste est prêt avant le premier jour. Lancer :  bash verifier_poste.sh
ok=0; ko=0
verifier() {  # verifier "nom" "commande" "conseil"
  if sortie=$(eval "$2" 2>&1); then echo "OK    $1 : $(echo "$sortie" | head -1)"; ok=$((ok+1))
  else echo "MANQUE $1 -> $3"; ko=$((ko+1)); fi
}
verifier "Python 3.12"   "python3.12 --version"            "installer Python 3.12 (python.org ou gestionnaire de paquets)"
verifier "Git"           "git --version"                   "installer Git"
verifier "Docker"        "docker --version"                "installer Docker Desktop ou équivalent"
verifier "Docker démarré" "docker info --format '{{.ServerVersion}}'" "démarrer Docker avant de lancer Airflow"
verifier "Astro CLI"     "astro version"                   "https://www.astronomer.io/docs/astro/cli/install-cli"
verifier "OpenSSL"       "openssl version"                 "installer OpenSSL (nécessaire pour la paire de clés)"
echo
echo "$ok vérifications réussies, $ko à corriger."
[ "$ko" -eq 0 ]
