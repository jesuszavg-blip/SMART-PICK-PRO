export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // 1. Servir el Manifest PWA oficial para Android y iOS
    if (url.pathname === '/manifest.json') {
      const manifest = {
        name: "Smart Pick Pro VIP",
        short_name: "SmartPick",
        start_url: "/",
        display: "standalone",
        background_color: "#0D0F14",
        theme_color: "#0D0F14",
        orientation: "portrait",
        icons: [
          {
            src: "https://raw.githubusercontent.com/jesuszavg-blip/SMART-PICK-PRO/main/assets/app_icon.jpg",
            sizes: "192x192 512x512",
            type: "image/jpeg",
            purpose: "any maskable"
          }
        ]
      };
      return new Response(JSON.stringify(manifest), {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        }
      });
    }

    // 2. Servir la WebApp a pantalla completa con soporte PWA
    const html = `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Smart Pick Pro VIP - Inteligencia Deportiva</title>
  
  <!-- Iconos de Aplicacion PWA -->
  <link rel="icon" type="image/jpeg" href="https://raw.githubusercontent.com/jesuszavg-blip/SMART-PICK-PRO/main/assets/app_icon.jpg">
  <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/jesuszavg-blip/SMART-PICK-PRO/main/assets/app_icon.jpg">
  <link rel="manifest" href="/manifest.json">
  
  <!-- Meta tags PWA -->
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="SmartPick VIP">
  <meta name="theme-color" content="#0D0F14">

  <style>
    html, body {
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      background-color: #0D0F14;
    }
    iframe {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      border: none;
      margin: 0;
      padding: 0;
      overflow: hidden;
    }
  </style>
</head>
<body>
  <iframe 
    src="https://smart-pick-pro.streamlit.app/?embed=true" 
    style="position:fixed;top:0;left:0;width:100%;height:100%;border:none;margin:0;padding:0;overflow:hidden;" 
    allow="camera; microphone; geolocation; autoplay; clipboard-write; encrypted-media">
  </iframe>
</body>
</html>`;

    return new Response(html, {
      headers: {
        "Content-Type": "text/html;charset=UTF-8"
      }
    });
  }
};
