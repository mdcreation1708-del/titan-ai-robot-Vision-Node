TiTaN AI Robot — Mobile Vision Node

Deploy this folder as a separate Vercel project using the default static-site settings. No render.yaml and no Python backend are needed here.

After deployment, open the Vision Node URL with your main backend URL as a query parameter:
https://YOUR-VISION-NODE.vercel.app/?api=https://YOUR-MAIN-DASHBOARD.vercel.app

Allow camera permission in the browser. The node will send JPEG frames and heartbeat requests to the configured main backend. The main backend package includes CORS response headers for this prototype.

IMPORTANT: The existing main backend stores frames in process memory and exposes an MJPEG stream. Vercel serverless functions may use different instances for uploads and stream requests, so a separate Vision Node alone cannot guarantee the dashboard will show video. A shared transport/storage or WebRTC relay is still needed for reliable live video on Vercel.
