# Exemples de rapports — quelques lignes chacun

**Tous les scénarios et chiffres ci-dessous sont fictifs.** Ils illustrent le
format d'un livrable, pas une recherche de marché, une certification ou une
investigation exécutée. Aucun client, compte, binaire ou service réel n'est visé.

## market-research

> **Question :** existe-t-il une opportunité pour un service fictif de location ?
> **Hypothèse de démonstration :** 100 lieux × 2 achats/an × 300 € = 60 000 €/an.
> **Fourchette illustrative :** 50–150 lieux → 30 000–90 000 €/an.
> **À vérifier :** nombre de lieux, fréquence et budget via sources primaires.
> **Décision :** ne pas traiter cette simulation comme un marché mesuré.

## research-reporting

> **Note de décision — projet fictif**
> Potentiel modélisé : 60 000 €/an ; données non vérifiées.
> Sensibilité principale : nombre de lieux acheteurs.
> Prochaine étape proposée : valider la demande avant de fixer un prix.
> Source : [hypothèses de démonstration ci-dessus](#market-research).

## backlog-execution

> **Périmètre autorisé fictif :** deux tâches, aucune publication automatique.
> ✓ Préparer un brief — preuve attendue : `brief.md` relu.
> ☐ Produire l'animation — bloqué : texte final non approuvé.
> **Bilan illustratif :** 1/2 ; pas de pourcentage de production inventé.

## rea-investigation

> **Exemple de restitution, REA non exécuté :**
> `ouvrir fichier → importDocument() → parseDocument() → aperçu`
> Artefact supposé : application de test appartenant à l'opérateur.
> Preuve à collecter : module, offset/ligne et référence de capture autorisée.
> Hypothèse : le décodage est local ; aucune conclusion réseau sans observation.

Ce flux inventé montre le niveau de concision attendu. Il ne provient pas d'une
sortie du moteur REA et ne justifie aucun contournement d'accès.

## reverse-api-investigation

> **Carte de contrat fictive :** `GET /v1/items?page=N` → collection paginée.
> **À confirmer :** schéma des réponses, pagination finale et erreurs.
> **Client visé :** configuration par environnement, jamais de secret embarqué.
> **Statut :** pas de requête réseau exécutée, pas de client validé.

Le [résumé structurel réel](outputs/api-summary.json) a été produit avec
`har-summary.mjs` à partir de [deux événements synthétiques](fixtures/request-events.json).
Il contient un hôte opaque, un endpoint et deux réponses HTTP 200. Il ne permet
**pas** d'inférer la sémantique du contrat ci-dessus : celle-ci est fictive et
nécessiterait des preuves autorisées supplémentaires.

## Outils de référence

- **REA 6.4.0** : [flux de restitution](#rea-investigation), démonstration textuelle,
  pas une session REA. [Intégration](../tools/rea/README.md).
- **Reverse API Engineer 0.14.0** : [contrat fictif](#reverse-api-investigation),
  via notre adaptation ; aucun lancement de l'agent amont ni secret en dur.
  [Évaluation](../tools/reverse-api-engineer/README.md).

[Retour à la galerie](README.md)
