# AI-assisted VFX: options, costs and licences

Use AI tools to remove tedious work, not to skip the integration and QA steps.
Every processed or generated element is listed in the delivery receipt with the
tool, version or job id, and licence basis.

## Higgsfield (cloud, spends credits)

Through the AE bridge or the Higgsfield MCP, depending on what the session
exposes:

| Capability | Use | Cautions |
| --- | --- | --- |
| Remove Background | subject isolation without a screen | check edges at 200% on hair and motion blur; trim to the used range first |
| Reframe | 16:9 → 9:16 / 1:2 deliveries | it tracks the subject, not your safe areas; re-check every title |
| Upscale | low-resolution plates before grading | upscale before grading and effects, never after |
| Edit Video / generation models (for example Seedance, Kling, Veo) | missing plates, B-roll, sky elements | generated media is a plate; copy and logos stay native; read the bridge's Seedance prompt contract before prompting |
| Hosted workflows `/Shot-Composer`, `/Shot-Cleanup` | guided composite or cleanup | less control over the AEP structure; re-audit the result |

Credit discipline: say what runs on which layer and range, wait for consent
unless the request already authorised that exact operation, one operation per
consent, no unrequested variants, and report failures once before retrying.
Commercial rights depend on the account's plan — flag once for client work.

## Local ComfyUI (offline, GPU-bound)

A local ComfyUI keeps confidential footage on the machine. On an 8 GB GPU,
prefer small/quantized models, short clips, low resolution passes and tiling;
expect long renders. Drive it by hand, or from an agent through the official
Comfy MCP (`Comfy-Org/comfy-mcp`, local connection) when installed separately.

| Task | Model family | Licence of commonly used weights (check the exact checkpoint) |
| --- | --- | --- |
| Background removal (stills, frames) | BiRefNet | MIT |
| Background removal (stills) | BRIA RMBG-2.0 | **CC BY-NC 4.0 — commercial use needs a BRIA agreement** |
| Segmentation/tracking masks | SAM 2 | Apache-2.0 |
| Video matting | MatAnyone | **S-Lab License 1.0 — non-commercial** |
| Depth maps (haze, defocus, 2.5D) | Depth Anything V2 | **Small: Apache-2.0; Base/Large: CC BY-NC 4.0** |
| Frame interpolation | RIFE | MIT |
| Upscaling | Real-ESRGAN | BSD-3-Clause |
| Video generation / inpainting | Wan 2.x | Apache-2.0 |

Licences above were checked during the toolbox's 2026-10 research and can
change; re-verify the specific checkpoint before client delivery.

Workflow rules:

1. Export frames or a ProRes/PNG intermediate from AE (never feed the
   long-GOP delivery file back in).
2. Fix seeds and record workflow JSON, model file names and hashes beside the
   outputs (`_planning/<MODULE>_BUILD/ai_vfx_ledger.json`).
3. Re-import results as image sequences at the plate's frame rate; confirm the
   frame count matches the source range.
4. Treat model output as a draft matte or plate: refine edges, colour and grain
   in AE and run the integration QA.

## Choosing between them

| Situation | Prefer |
| --- | --- |
| Confidential client footage | native AE or local models |
| Hair-heavy subject, deadline, credits available | Higgsfield Remove Background, then refine |
| Commercial deliverable with a model output inside | a commercially licensed model or a native method |
| Need a plate that does not exist | generation, then full integration in AE |
| Simple, static cleanup | Content-Aware Fill or a tracked patch |
