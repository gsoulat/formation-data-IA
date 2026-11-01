# Fiche juridique — lire le RGPD sans être juriste

Une page pour la veille du jour 1. Elle explique les mots et la méthode ; elle ne répond pas à la place de votre note. Chaque affirmation de votre note cite le texte officiel, pas cette fiche.

## 1. Les mots à connaître

| Mot | Ce qu'il veut dire | Question à se poser |
|---|---|---|
| **Donnée personnelle** | toute information sur une personne identifiable, directement (nom) ou en croisant d'autres informations (identifiant, date de naissance + dépôt) | peut-on retrouver la personne, seule ou en combinant ? |
| **Traitement** | toute opération sur ces données : collecter, stocker, copier, consulter, supprimer | un `SELECT` est-il un traitement ? (oui) |
| **Finalité** | le but du traitement : payer les salaires, organiser les services | pour quoi fait-on cela ? |
| **Responsable du traitement** | celui qui **décide** pourquoi et comment les données sont traitées | qui décide ? |
| **Sous-traitant** | celui qui **exécute** pour le compte du responsable, sans décider des finalités | qui exécute sur instruction ? |
| **Base légale** | la raison qui autorise le traitement : contrat, obligation légale, intérêt légitime, consentement… | sur quoi s'appuie le traitement ? |
| **Établissement** | une installation stable d'une entreprise dans un pays : filiale, bureau, équipe | où l'entreprise exerce-t-elle réellement ? |
| **Autorité de contrôle** | l'organisme qui veille au respect du RGPD dans un pays : en France, la CNIL | à qui rend-on des comptes ? |
| **Durée de conservation** | combien de temps on garde la donnée, fixée selon la finalité | quand doit-elle disparaître, ou sortir de la base active ? |
| **Base active / archivage intermédiaire** | la base où l'on travaille au quotidien / un stockage séparé, à accès restreint, pour les données qu'on doit garder sans s'en servir | une donnée qui ne sert plus doit-elle rester sous les yeux de tous ? |
| **Transfert hors UE** | envoyer ou héberger des données dans un pays hors de l'Union européenne | où sont physiquement les données ? |

## 2. Qui décide, qui exécute

Un exemple qui n'est pas le vôtre : une chaîne de librairies installée à Lyon gère le fichier de ses clients canadiens. Elle décide des finalités (fidélité, facturation). Elle stocke ce fichier chez un hébergeur, qui ne fait qu'exécuter.

```
   Librairie (Lyon)  ──── décide des finalités ────►  RESPONSABLE DU TRAITEMENT
          │
          │ confie le stockage, sur instruction
          ▼
     Hébergeur cloud ──── exécute, ne décide pas ───►  SOUS-TRAITANT
```

Le mot qui compte est **décider**. Pour votre cas, relisez le contexte du brief : qui décide désormais de ce que deviennent les données des chauffeurs ? Et Snowflake, que fait-il ?

## 3. Lire l'article 3 (le champ d'application territorial)

L'article 3 répond à une seule question : le RGPD s'applique-t-il, alors que les personnes ne sont pas en Europe ? Il a deux paragraphes principaux, et il suffit qu'**un seul** s'applique.

- **3.1** : le RGPD s'applique au traitement fait *dans le cadre des activités d'un établissement* dans l'Union, que le traitement ait lieu dans l'Union ou non. Ce paragraphe regarde **l'entreprise**.
- **3.2** : le RGPD s'applique aussi à une entreprise *sans établissement* dans l'Union, si elle vise des personnes qui se trouvent dans l'Union (leur vendre quelque chose, suivre leur comportement). Ce paragraphe regarde **les personnes**.

Méthode : pour chacun des deux paragraphes, écrivez « oui / non, parce que… » avec un fait du contexte. Le texte se lit sur EUR-Lex (lien dans les ressources, chercher « Article 3 »). Les lignes directrices 3/2018 du CEPD sont longues : lisez seulement leur partie sur le critère d'établissement (article 3, paragraphe 1), et regardez ses exemples.

## 4. Le référentiel CNIL « gestion du personnel » : quoi lire

Ne lisez pas tout. La partie utile pour le contrat est la **section 7, « Durées de conservation »** (pages 10 à 12 du PDF). Cherchez-y deux choses :

1. ce qui distingue la **base active** de l'**archivage intermédiaire** ;
2. la ligne du tableau sur le **registre unique du personnel** : durée, et texte sur lequel elle s'appuie.

Puis posez-vous la question qui fait la différence : la durée vient-elle du RGPD, ou du code du travail français ? Le RGPD ne fixe aucune durée en jours ou en années : il impose qu'elle soit justifiée par la finalité. Une durée qui vient du droit du travail français se discute pour des contrats signés à New York ; elle se justifie alors par les obligations locales, et se documente.

## 5. Trois pièges

- **Recopier le texte** : une fiche dit ce que le texte change pour vos tables, avec vos mots.
- **Citer un blog** : un article peut vous signaler un texte, mais la fiche cite le texte officiel (EUR-Lex, CNIL, CEPD), avec sa date.
- **Trancher seul une vraie question juridique** : notez-la dans la section 5 de la note (« Ce que la veille ne tranche pas »), avec à qui vous la poseriez.
