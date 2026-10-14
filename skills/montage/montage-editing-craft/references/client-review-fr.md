# Révisions client et notes de livraison (modèles en français)

## Tableau de commentaires (une ligne par note)

| # | Version | Code temporel | Commentaire du client | Décision | Statut |
| --- | --- | --- | --- | --- | --- |
| 1 | v01 | 00:00:04:12 | « Le prix est trop petit » | agrandir à 44 px de hauteur de capitale | fait v02 |
| 2 | v01 | 00:00:12:00 | « Changer la musique » | 3 options proposées, choix B | fait v02 |

- Regrouper toutes les notes d'une ronde avant de modifier.
- Signaler ce qui sort de l'entente (nouvelle version, nouveau format).
- Une note ambiguë → une question précise au client, avec deux options.

## Message de livraison (aperçu)

> Bonjour [Prénom],
>
> Voici la version **v02** de [projet] : [lien ou fichier].
>
> - Format : 516 × 1032 px, 30 i/s, 20 secondes, en boucle, sans son.
> - Modifications : notes 1 à 7 de la ronde précédente.
> - Vérifications faites : décodage complet du fichier (600 images), boucle
>   sans saut, textes relus, polices et médias autorisés.
> - À vérifier de votre côté : affichage sur l'écran réel et validation finale
>   des mentions (prix, taxes, conditions).
>
> Merci de regrouper vos commentaires avec le code temporel affiché.
>
> [Signature]

## Livraison finale

- Fichiers nommés `CLIENT_PROJET_FORMAT_LxH_IPSp_vNN.mp4`.
- Rapport QC (JSON) et planche contact conservés dans le projet.
- Archive : projet, médias, polices, licences musique/SFX, rapports.
- L'approbation interne ne remplace pas l'approbation écrite du client.
