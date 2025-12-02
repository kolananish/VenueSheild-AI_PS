# VenueShield AI

**Real-Time Safety Intelligence for Venues**

VenueShield AI is an AI-powered safety platform that detects risks in real-time using your existing security cameras. Designed for arenas, theaters, convention centers, universities, nightclubs, and stadiums.

![Next.js](https://img.shields.io/badge/Next.js-16-black?style=for-the-badge&logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=for-the-badge&logo=typescript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-4-38bdf8?style=for-the-badge&logo=tailwindcss)
![React](https://img.shields.io/badge/React-19-61dafb?style=for-the-badge&logo=react)

## ✨ Features

- **Real-Time Crowd Monitoring** - AI-powered crowd density detection and flow analysis
- **Multi-Camera Dashboard** - View all camera feeds with live status indicators
- **Incident Management** - Track, respond to, and resolve security incidents
- **Predictive Analytics** - AI forecasting for crowd patterns and potential issues
- **Compliance Tracking** - Monitor regulatory requirements and certifications
- **Smart Alerts** - Automated notifications based on configurable thresholds

## 🚀 Getting Started

### Installation

```bash
# Install dependencies
pnpm install

# Start the development server
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) to view the landing page.

### Demo Dashboard

Visit [http://localhost:3000/demo](http://localhost:3000/demo) to explore the interactive dashboard with:

| Page                | URL                | Description                                                        |
| ------------------- | ------------------ | ------------------------------------------------------------------ |
| **Dashboard**       | `/demo`            | Overview with key metrics, camera feeds, alerts, and zone status   |
| **Camera Feeds**    | `/demo/cameras`    | Full camera grid with search, filters, and fullscreen view         |
| **Crowd Analytics** | `/demo/analytics`  | Occupancy trends, AI predictions, zone analytics, demographics     |
| **Incidents**       | `/demo/incidents`  | Incident management with timeline, status tracking, and resolution |
| **Compliance**      | `/demo/compliance` | Regulatory requirements, certificates, and audit history           |

## 📁 Project Structure

```
├── app/
│   ├── demo/
│   │   ├── page.tsx           # Main dashboard
│   │   ├── layout.tsx         # Shared demo layout with sidebar
│   │   ├── cameras/           # Camera feeds page
│   │   ├── analytics/         # Crowd analytics page
│   │   ├── incidents/         # Incident management page
│   │   └── compliance/        # Compliance dashboard page
│   ├── globals.css            # Global styles
│   ├── layout.tsx             # Root layout
│   └── page.tsx               # Landing page
├── components/
│   ├── ui/                    # Reusable UI components (shadcn/ui)
│   ├── demo-dashboard.tsx     # Dashboard content component
│   ├── hero-section.tsx       # Landing page hero
│   ├── features-section.tsx   # Landing page features
│   └── ...                    # Other landing page sections
├── lib/
│   └── utils.ts               # Utility functions
└── public/
    └── images/
        ├── surveillance-*.jpg # Demo camera feed images
        └── venueshield-logo.png
```

## 🎨 Tech Stack

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 4
- **UI Components**: shadcn/ui + Radix UI
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Charts**: Custom SVG visualizations

## 📜 Available Scripts

```bash
pnpm dev          # Start development server
pnpm build        # Build for production
pnpm start        # Start production server
pnpm lint         # Run ESLint
pnpm type-check   # Run TypeScript type checking
pnpm format       # Check code formatting
pnpm format-write # Format code with Prettier
```

## 🔮 Roadmap

- [ ] Backend API integration
- [ ] Real camera feed support
- [ ] User authentication
- [ ] Custom alert configuration
- [ ] Report generation
- [ ] Mobile app

## 📄 License

MIT
