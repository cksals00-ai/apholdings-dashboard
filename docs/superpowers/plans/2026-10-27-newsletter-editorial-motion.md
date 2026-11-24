# AP News editorial motion implementation
Goal: approved editorial newsletter layout with animated brand cover from October28, no paid API.
1. Add opt-in v2 shared HTML/email renderer; validate cover paths/assets and use static poster in PDF. Preserve legacy output.
2. Create deterministic abstract orbit GIF and static poster locally, preserving existing AP logo. Add pause/reduced-motion web behavior.
3. Include both cover assets in bundle/public verification; verify same summary/fact/insight/takeaway in all channels without story action.
4. Regression tests, render all preview PDF pages, 390px/desktop preview and GIF frames. Do not publish preview as real news or resend mail.
5. Deploy renderer/assets, update daily preparation automation and README to require v2 from October28.
