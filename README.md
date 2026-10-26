# TikTok Documentary Agent — free review-only cloud workflow

This repository generates original, captioned vertical documentary videos in GitHub Actions. **It does not post to TikTok or Metricool.** First three videos require human review; publication remains disabled until explicit approval and a tested integration.

## Run in GitHub without your computer

1. Open **Actions → Generate review-only documentary → Run workflow**.
2. Choose a topic (universe, history, wars, evolution, biology, future).
3. Wait for the workflow to finish. Open its run and download **documentary-review-...** under Artifacts.
4. Watch the MP4 and read `metadata.json` before approving anything.

A daily scheduled run is configured, but GitHub scheduled runs are best-effort and may be delayed or disabled after inactivity. Workflow jobs use free GitHub-hosted runners for public repositories, subject to GitHub policy and quotas. Artifacts expire after 7 days. This is **not** a persistent server or a guaranteed hourly generator.

## Design

- Pillow procedural original animations, including astronomical diagrams and motion graphics.
- Microsoft Edge neural TTS via edge-tts (network service, may be unavailable).
- FFmpeg video/audio muxing.
- Scripted, curated educational facts, with reference URLs in metadata. Not independently live fact-checked.
- 540×960 output (9:16) at 12 fps to fit free runner limits.
- Captions are rendered directly into the video.
- No HeyGen logo, HeyGen asset, stock footage, or watermark added by this renderer.
- Synthetic imagery is marked **ILLUSTRATION / SIMULATION**.

**Limitations:** The animation is stylized 2.5D, not photorealistic 3D. It is not real telescope footage. Video duration depends on narration length. The initial scripts are templates and must be editorially checked, especially before posting. No breaking-news automation is included; future content is explicitly speculative. The free Edge TTS service has no uptime guarantee.

## Safety

Do not commit credentials, tokens, or private video assets. No automatic publishing is enabled. The workflow can be disabled in GitHub Actions. To publish, separately connect an authorized Metricool workflow after video review and plan-limit checks.
