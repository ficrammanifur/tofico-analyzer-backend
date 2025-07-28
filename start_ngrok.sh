#!/bin/bash
echo "🌐 Starting ngrok tunnel..."
echo "📡 Forwarding localhost:8000 to public URL"
echo ""

# Start ngrok
ngrok http 8000

# Instructions will be shown after ngrok starts
echo ""
echo "📋 Next steps:"
echo "1. Copy the ngrok URL (https://xxxxx.ngrok-free.app)"
echo "2. Update API_BASE_URL in script.js"
echo "3. Upload frontend to GitHub Pages"
