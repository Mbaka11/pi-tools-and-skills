# Galerie — exemples très courts

**Voir ce que chaque skill peut produire**, sans ouvrir un projet client.
Les animations durent **3 secondes**. Tout a été créé pour cette galerie :
formes, textes fictifs, textures procédurales et sons synthétiques.

- **Sortie réelle** : fichier effectivement produit par le helper indiqué.
- **Maquette** : aperçu du résultat visé, pas une exécution AE, Premiere,
  Remotion, REA ou d'un service payant. Aucun AEP natif n'est livré ici.
- **Exemple fictif** : format de restitution, pas une observation vérifiée.

Les GIF sont volontairement petits et à 10 i/s pour GitHub ; ce ne sont pas
les masters de livraison. Cliquer sur les fichiers MP4/WAV pour les lire ou
les télécharger si GitHub n'affiche pas de lecteur. Les trois secondes servent
à démontrer un geste, pas à recommander la durée d'une publicité réelle.

## ae-vox-editorial

**Maquette · 3 s** — papier, surlignage, carte découpée et mouvement décalé.

![Collage éditorial synthétique](media/ae-vox.gif)

Demande courte : « Fais apparaître une idée avec un surlignage et une carte papier. »
[Skill](../skills/after-effects/ae-vox-editorial/SKILL.md)

## ae-expressions-rigs

**Maquette · 3 s** — le cartouche s'adapte lorsque le titre s'allonge.

![Boîte redimensionnée autour du texte](media/ae-rig.gif)

Extrait pour **Rectangle Path › Size** dans AE, à valider dans le projet :

```js
var b = thisComp.layer("TITRE").sourceRectAtTime(time, false);
[b.width + 36, b.height + 24];
```

Le GIF est dessiné avec Pillow : ses métriques ne sont pas celles d'AE.
Position/parentage du rectangle : suivre la
[bibliothèque de mise en page](../skills/after-effects/ae-expressions-rigs/references/layout-text-led.md).

## ae-vfx-compositing

**Maquette · 3 s** — avant/après d'un remplacement d'écran sur un décor fictif.

![Aperçu de remplacement d'écran](media/ae-vfx.gif)

Montre le principe d'incrustation en perspective, pas un tracking exécuté ni
un test de Keylight ou de Roto Brush.
[Skill](../skills/after-effects/ae-vfx-compositing/SKILL.md)

## ae-production-workflow

**Sortie réelle du vérificateur de manifeste**, sur un fichier texte synthétique :

```json
{"ok": true, "entriesChecked": 1, "canonicalOk": true, "failures": []}
```

[Rapport](outputs/delivery-check.json) · [Manifeste](outputs/delivery-manifest.json) ·
[Fixture canonique](outputs/canonical.txt).
Cela prouve une vérification de taille/hash, **pas** la validité d'un AEP ni une
inspection native. Exemples checkpoint/RAM : [outils](tools.md#helpers-ae).
[Skill](../skills/after-effects/ae-production-workflow/SKILL.md)

## led-signage-content

**Sortie réelle · 3 s · 516×1032 · 30 i/s · sans audio** — un message lisible
et un élément en mouvement périodique, exportés avec `led_tool.py`.

![Aperçu réduit de la boucle LED](media/led-poster.png)

[Lire la boucle MP4](media/led-loop.mp4) · [Mire au pixel près](media/led-testcard.png) ·
[Guides pour trois panneaux](media/led-guides.png) · [Contrôle du profil](outputs/led-check.json).
La vignette est réduite ; les fichiers de livraison restent à leur taille exacte.
Le matériel, la luminosité et la synchronisation physique n'ont pas été testés.
[Skill](../skills/montage/led-signage-content/SKILL.md)

## video-delivery-qc

**Sortie réelle** — les 90 images de la boucle ci-dessus ont été décodées ;
la jonction de boucle et l'absence d'audio ont été vérifiées automatiquement.

![Contact sheet extraite du fichier encodé](media/qc-contact.png)

[Rapport JSON complet](outputs/media-qc.json), avec hash du MP4, SSIM de jonction,
contrôles, avertissements et limites. `ok` ne certifie pas un écran réel.
[Skill](../skills/montage/video-delivery-qc/SKILL.md)

## sound-design-sfx

**Sortie réelle · 3 s** — souffle court → impact → carillon, placés par
`sfx_place.py` aux images **9, 30 et 60** d'une timeline à 30 i/s.

[Écouter le WAV 48 kHz / 24 bits stéréo](media/sfx.wav) ·
[Lire le MP4 avec son](media/sfx-preview.mp4) ·
[Placement des cues](outputs/sfx-cues.json) · [Mesure audio](outputs/sfx-qc.json).

Sons originaux synthétisés localement, aucun échantillon de bibliothèque.
Le MP4 ajoute le stem à la maquette de montage : impact sur la coupe à 1 s,
carillon sur l'arrivée du titre à 2 s.
Les mesures et le décodage ne remplacent pas une écoute humaine.
[Skill](../skills/montage/sound-design-sfx/SKILL.md)

## montage-editing-craft

**Maquette · 3 s** — plan large, détail, titre : trois images, une progression.

![Mini-montage synthétique en trois plans](media/editing.gif)

**Sortie réelle de `srt_check.py`** :
`Bonjour : une idée !` → espaces insécables avant `:` et `!`, dans une copie.
[Avant](fixtures/captions.srt) · [Après](outputs/captions-fixed.srt) ·
[Rapport avant](outputs/captions-before.json) · [Rapport après](outputs/captions-after.json).
L'original n'est pas modifié. Ce n'est pas un export Premiere.
[Skill](../skills/montage/montage-editing-craft/SKILL.md)

## vox-explainer-pipelines

**Maquette de structure · 3 s** — question → indice → réponse.

![Micro-explainer à trois beats](media/explainer.gif)

Cette prévisualisation originale illustre le beat sheet ; elle **n'a pas été
rendue avec les pipelines amont**. Pour leurs démonstrations, voir le
[README amont épinglé](https://github.com/jaredcassoutt/vox-editorial/tree/f394e925f7ccbd6df3e6b3403fcb260194bbece3).
Aucun extrait externe n'a été recopié ni aucune voix générée.
[Skill](../skills/montage/vox-explainer-pipelines/SKILL.md)

## market-research

**Exemple fictif** : « 100 lieux × 2 achats/an × 300 € = 60 000 €/an de potentiel
modélisé ; trois hypothèses à vérifier. » [Mini-étude](reports.md#market-research) ·
[Skill](../skills/market-research/SKILL.md).

## research-reporting

**Exemple fictif** : « Données non vérifiées ; valider la demande avant de fixer
le prix. » [Note de décision](reports.md#research-reporting) ·
[Skill](../skills/research-reporting/SKILL.md).

## backlog-execution

**Exemple fictif** : « Brief prêt ; animation bloquée par le texte final ;
1 tâche sur 2. » [Mini-bilan](reports.md#backlog-execution) ·
[Skill](../skills/backlog-execution/SKILL.md).

## rea-investigation

**Exemple fictif, moteur non exécuté** :
`ouvrir fichier → importDocument() → parseDocument() → aperçu`.
[Mini-rapport et limites](reports.md#rea-investigation) ·
[Skill](../skills/rea-investigation/SKILL.md).

## reverse-api-investigation

**Sortie réelle du helper**, sur deux événements fabriqués : un hôte opaque,
un endpoint, deux réponses 200, aucune URL brute publiée dans le résumé.
[Résumé JSON](outputs/api-summary.json) · [Contrat fictif](reports.md#reverse-api-investigation) ·
[Skill](../skills/reverse-api-investigation/SKILL.md).

## Outils, provenance et reproduction

- [Un micro-exemple par outil/helper inclus](tools.md).
- [Micro-exemples des outils seulement catalogués](../docs/montage-catalog.md#micro-examples-for-catalog-only-tools)
  — intentions illustratives, pas des moteurs installés ou exécutés.
- [Manifeste des exemples](manifest.json) : couverture, provenance, tailles et SHA-256.
- [Environnement de génération](outputs/build-info.json) : aucun appel cloud,
  aucun média client, aucun rendu natif AE. Polices système utilisées au rendu,
  sans redistribution des fichiers de police.
- Les exemples originaux suivent [RIGHTS.md](../RIGHTS.md) (`UNLICENSED`).
  Aucun média tiers n'est redistribué ; les snapshots MIT restent inchangés.

Pour recréer les médias et les sorties des helpers dans un **nouveau** dossier :

```sh
# Python + Pillow >= 9.2 + FFmpeg/libx264 + Node disponibles séparément.
python examples/build.py --out .local/examples-preview
# Si nécessaire : ajouter --font /chemin/vers/une-police-autorisee.ttf
npm test
```

Le générateur n'installe rien, ne supprime rien et refuse un dossier déjà existant.
Il n'écrit jamais directement dans la galerie publiée. Les octets des images et
encodages peuvent varier avec la version des moteurs et de la police ; revoir les
sorties avant de mettre à jour les hashes. Aucun seuil QC n'est modifié pour faire
passer une nouvelle génération.
