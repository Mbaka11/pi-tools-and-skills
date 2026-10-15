# Un exemple très court par outil inclus

Les liens ci-dessous pointent sur des sorties synthétiques réellement générées,
ou portent explicitement la mention **illustratif / non exécuté**.
Les moteurs tiers ne sont pas installés par ces exemples.

## Helpers montage

| Outil | Exemple de résultat |
| --- | --- |
| [`led_tool.py`](../skills/montage/led-signage-content/scripts/led_tool.py) | [Boucle 3 s](media/led-loop.mp4), [mire](media/led-testcard.png), [guides](media/led-guides.png) ; à 4 m/P1.86, hauteurs de capitales **18 / 26 / 44 px** ([calcul](outputs/text-size.json)). |
| [`media_qc.py`](../skills/montage/video-delivery-qc/scripts/media_qc.py) | [90 images décodées, pas d'audio, jonction mesurée](outputs/media-qc.json) + [planche de contrôle](media/qc-contact.png). |
| [`sfx_place.py`](../skills/montage/sound-design-sfx/scripts/sfx_place.py) | [Stem de 3 s](media/sfx.wav), trois cues à **0,3 / 1 / 2 s** ([extrait du résultat](outputs/sfx-cues.json)). |
| [`srt_check.py`](../skills/montage/montage-editing-craft/scripts/srt_check.py) | [Copie corrigée](outputs/captions-fixed.srt) ; [0 erreur après correction](outputs/captions-after.json). |

## Helpers AE

| Outil | Exemple de résultat |
| --- | --- |
| [`verify-delivery-manifest.py`](../skills/after-effects/ae-production-workflow/scripts/verify-delivery-manifest.py) | [Résultat réel](outputs/delivery-check.json) : `ok=true`, un fichier texte vérifié, aucun AEP impliqué. |
| [`checkpoint-aep.ps1`](../skills/after-effects/ae-production-workflow/scripts/checkpoint-aep.ps1) | **Illustratif, non exécuté** : `Demo_before_title_YYYYMMDD_HHmmss.aep`, copie horodatée dont le hash doit égaler celui du projet sauvegardé. Pas de faux AEP publié. |
| [`ram-snapshot.ps1`](../skills/after-effects/ae-production-workflow/scripts/ram-snapshot.ps1) | **Illustratif, non exécuté** : « Mémoire libre sous le seuil → pause, aucun nouveau rendu ». Aucun diagnostic de cette machine n'est publié. |

## Investigation et moteurs

| Outil | Exemple de résultat |
| --- | --- |
| [`har-summary.mjs`](../skills/reverse-api-investigation/scripts/har-summary.mjs) | [Résumé réel de deux événements fictifs](outputs/api-summary.json) : `host_1`, `endpoint_1`, `requests=2`, sans URL/cookie/token. |
| [REA](../tools/rea/README.md) | [Chaîne d'import fictive](reports.md#rea-investigation) ; moteur non exécuté. |
| [Reverse API Engineer](../tools/reverse-api-engineer/README.md) | [Mini-carte d'API fictive](reports.md#reverse-api-investigation) ; agent amont non exécuté, aucun secret en dur. |
| [Vox editorial / Remotion et Python](../vendor/vox-editorial/README.md) | [Maquette originale à trois beats](README.md#vox-explainer-pipelines), pas un rendu des scripts amont. |
| [Cinematic score and SFX](../vendor/cinematic-score-and-sfx/README.md) | **Illustratif** : `révélation → souffle ; coupe → impact ; conclusion → carillon`. [Audio original](media/sfx.wav) produit par notre helper, pas par un fournisseur amont. |

## Utilitaires de maintenance

| Outil | Exemple très court |
| --- | --- |
| [`check.mjs`](../scripts/check.mjs) | `node scripts/check.mjs` → exemple de forme `{"ok":true,"skills":["…"],"errors":[]}` ; le résultat actuel dépend des fichiers inspectés. |
| [`check-examples.mjs`](../scripts/check-examples.mjs) | Vérifie qu'un média est déclaré, borné en taille et conforme à son SHA-256 ; rejette une vidéo ajoutée hors manifeste. |
| [`check-updates.mjs`](../scripts/check-updates.mjs) | **Illustratif** : « version épinglée inchangée / mise à jour disponible » ; aucune vérification réseau n'est simulée comme actuelle. |
| [`fetch-source.mjs`](../scripts/fetch-source.mjs) | `node scripts/fetch-source.mjs vox-editorial` → plan de récupération au commit épinglé ; pas de téléchargement sans `--fetch`. |
| [`upstreams.mjs`](../scripts/upstreams.mjs) | Bibliothèque interne : lecture de `tools/upstreams.lock.json`, validation du pin et résolution sûre du chemin d'une source. |
| [`examples/build.py`](build.py) | Génère cette [galerie](README.md) dans un dossier neuf avec Pillow/FFmpeg ; refuse l'écrasement, sans cloud ni installation implicite. |

[Retour à la galerie](README.md)
