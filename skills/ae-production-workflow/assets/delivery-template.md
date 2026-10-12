# Livraison — <Module> <Version>

## État livré

- Canonique : `<path/to/project.aep>`
- Composition master : `<MASTER_COMP>`
- Format : `<width> × <height>, <fps> i/s`
- Durée : `<seconds> s / <frames> images`
- Backup final exact : `<path>`
- SHA-256 canonique/backup : `<hash>`
- État AE laissé : `<ouvert propre | fermé proprement>`

## Organisation AEP

```text
<ROOT_FOLDER>/
  01_COMPOSANTS/
  02_ASSETS/
  03_CONTROLES/
<MASTER_COMP>
```

Décrire les composants créés et les modules protégés inchangés.

## Direction appliquée

- Logo : `<mesures>`
- Typographie : `<fontes et substitution>`
- Palette : `<couleurs>`
- Safe area : `<limites et maximum mesuré>`
- Système de révélation : `<mattes/easing>`
- Variations spécifiques : `<liste>`

## Copy couverte

Lister chaque message obligatoire et toute formulation sensible conservée.

## Médias et montage

- Source empaquetée : `<path>`
- SHA-256 : `<hash>`
- Source timebase/fps/durée/images : `<timebase, rational fps, values>`
- IN : `<source frame index + exact PTS seconds>`
- OUT : `<source frame index + exact PTS seconds + policy>`
- Lecture timeline : `<timeline frame index + fps + seconds>`
- Vitesse/interprétation : `<values>`
- Source outro : `<preserved/changed>`
- Vérification audio : `<human audition | waveform only | not verified>`

## Aperçu complet

`<path/to/preview.mp4>`

- Codec : `<codec>`
- Dimensions/fps : `<values>`
- Images décodées : `<count>`
- Audio : `<codec/rate/channels>`
- Taille : `<bytes>`
- SHA-256 : `<hash>`
- Décodage complet : `<pass/fail>`

## QA native

Rapport : `<native_audit.json>`

- Fontes manquantes/substituées : `<count>`
- Erreurs d'expression : `<count>`
- Médias manquants : `<count>`
- `_QA_TEMP*` résiduels : `<count>`
- File de rendu résiduelle : `<count>`
- Textes hors safe area : `<count>`
- Problèmes de mattes/keyframes : `<count>`

## Test d'édition réversible

- Élément testé : `<comp/layer/control>`
- Valeur temporaire : `<value>`
- Mesures : `<width/right/etc>`
- Sortie : `<path>`
- Original restauré : `<yes/no>`
- Temp supprimé : `<yes/no>`

## Checkpoints

- Avant mutation : `<path>`
- Statique : `<path>`
- Motion : `<path>`
- Final exact : `<path>`

Manifestes et empreintes : `<delivery_manifest.json>`. Le manifeste doit contenir `canonical`, `canonical_sha256` et un tableau non vide `files[]` avec chemins relatifs, tailles exactes et SHA-256.

## Limites restantes

- `<human audio audition>`
- `<player/codec>`
- `<physical display/readability/color>`
- `<audio policy/sync>`
- `<remaining modules/global assembly>`
