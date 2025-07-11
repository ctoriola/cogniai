# Railway Deployment Guide - Optimized for 4GB Limit

## 🚀 Quick Deploy

1. **Connect to Railway**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login to Railway
   railway login
   
   # Link your project
   railway link
   ```

2. **Deploy**
   ```bash
   railway up
   ```

## 📦 Size Optimizations Applied

### Backend Optimizations
- ✅ **Replaced heavy ML packages**: Removed `transformers` and `torch` (~2GB)
- ✅ **Lightweight AI**: Using `scikit-learn` instead (~50MB)
- ✅ **Alpine Linux**: Smaller base image (~100MB vs ~500MB)
- ✅ **Multi-stage build**: Optimized Docker layers
- ✅ **Dockerignore**: Excluded unnecessary files

### Frontend Optimizations
- ✅ **Minimal dependencies**: Removed unused packages
- ✅ **Static build**: React build is served from Flask
- ✅ **No separate container**: Frontend served by backend

## 🔧 Environment Variables

Set these in Railway dashboard:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://... (Railway will provide this)
```

## 📊 Expected Image Size

- **Before**: ~5.7GB (exceeded 4GB limit)
- **After**: ~800MB-1.2GB (well under 4GB limit)

## 🛠️ Manual Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Optimized for Railway deployment"
   git push origin main
   ```

2. **Connect to Railway**
   - Go to [railway.app](https://railway.app)
   - Create new project
   - Connect GitHub repository
   - Railway will auto-detect and deploy

3. **Add Postgres Database**
   - In Railway dashboard, click "New"
   - Select "Database" → "PostgreSQL"
   - Railway will provide `DATABASE_URL`

4. **Set Environment Variables**
   - Go to project settings
   - Add `SECRET_KEY` variable
   - Railway will auto-set `DATABASE_URL`

## 🔍 Troubleshooting

### If deployment fails:
1. Check Railway logs for errors
2. Ensure all files are committed to Git
3. Verify environment variables are set
4. Check if database is properly connected

### If image is still too large:
1. Remove any remaining large files
2. Check `.dockerignore` is working
3. Consider removing unused dependencies

## 📈 Monitoring

- **Logs**: View in Railway dashboard
- **Metrics**: Railway provides basic monitoring
- **Database**: Use Railway's PostgreSQL dashboard

## 🚀 Production Tips

1. **Scale**: Railway auto-scales based on traffic
2. **Custom Domain**: Add in Railway dashboard
3. **SSL**: Railway provides automatic HTTPS
4. **Backups**: Railway handles database backups

## 💰 Cost Optimization

- **Free Tier**: 500 hours/month
- **Pay-as-you-go**: $0.000463 per GB-hour
- **Database**: $5/month for Postgres

## 🔄 Updates

To update your deployment:
```bash
git add .
git commit -m "Update message"
git push origin main
# Railway will auto-deploy
```

## 📞 Support

- Railway Docs: https://docs.railway.app
- Discord: https://discord.gg/railway
- GitHub Issues: For code-specific issues 