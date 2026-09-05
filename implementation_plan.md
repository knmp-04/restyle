# Restyle: Intelligent Wardrobe Utilization System - Architecture & Plan

This document outlines the proposed system architecture, technology stack, and detailed development roadmap for the **Restyle** platform, fulfilling the requirement for an intelligent wardrobe management and outfit recommendation system.

## 1. Feature Separation

### Minimum Viable Product (MVP)
* **User Authentication:** Secure signup/login.
* **Wardrobe Digitization:** Upload clothing images from the device.
* **Automated Tagging (AI):** Computer vision via APIs to remove backgrounds and extract attributes (color, category, style, season).
* **Wardrobe Organization:** Categorize, filter, and search clothing items.
* **Outfit Recommendations:** API-driven embedding or rule-based suggestions for outfits.
* **Restyle Suggestions:** Suggest new ways to wear specific items.
* **Utilization Tracking:** Track how often items are worn to promote sustainability.

### Future Features
* **Virtual Try-On:** Generative AI to visualize how items look on the user.
* **Advanced Color Analysis:** Color-theory-based recommendations matching user skin tone/season.
* **Social/Community Features:** Share outfits, seek feedback.
* **E-commerce Integration:** Suggest sustainable purchases to fill wardrobe gaps.
* **Self-hosted AI Models:** Migration from managed APIs to self-hosted models (U-2-Net, CLIP) to reduce costs at scale.

## 2. System Architecture

A robust Client-Server architecture focused on a seamless web experience.

* **Frontend & Backend (Full-stack Web App):** A responsive, mobile-first Web Application built with Next.js. It handles user interactions, image uploads, server-side rendering, and API routes.
* **AI Processing Layer:** Integration with Managed APIs (OpenAI Vision, Remove.bg) for fast, reliable image processing and background removal.
* **Database Layer:** Relational DB for user and wardrobe data, with a unified storage solution for processed images.

## 3. Technology Stack

* **Full-stack Framework:** Next.js (React) for both frontend UI and backend API routes.
* **Styling:** TailwindCSS (for rich, dynamic styling) and Framer Motion (for micro-animations and premium UI feel).
* **Database:** PostgreSQL (managed via Supabase or Neon), accessed via Prisma or Drizzle ORM.
* **Storage:** Cloudinary (excellent for on-the-fly image transformations) or AWS S3.
* **AI/CV APIs:** Remove.bg API (background removal), OpenAI Vision API (attribute classification and outfit logic).
* **Authentication:** Clerk or Supabase Auth.

## 4. Detailed Development Roadmap

The project is divided into 5 small, actionable milestones, starting with the simplest working MVP.

### Milestone 1: Foundation & Authentication
* **Objective:** Initialize the project repository and establish secure user access.
* **Features:** Next.js setup, UI design system configuration, User Signup/Login/Logout.
* **Files/Modules Required:**
  * `src/app/layout.tsx`, `src/app/page.tsx` (Landing page)
  * `src/middleware.ts` (Route protection)
  * `tailwind.config.ts`, `src/styles/globals.css`
* **Technologies:** Next.js (App Router), TailwindCSS, Clerk/Supabase Auth.
* **Dependencies:** None.
* **Testing Requirements:** Verify public vs. protected routing. Ensure users can successfully register, log in, and log out.

### Milestone 2: Wardrobe Digitization & Storage
* **Objective:** Enable users to upload clothing images and store them securely in the cloud and database.
* **Features:** Image upload UI component, cloud storage integration, basic database schema for clothing items.
* **Files/Modules Required:**
  * `src/components/UploadForm.tsx`
  * `src/app/api/upload/route.ts`
  * DB schema (e.g., `schema.prisma` for User and Item models)
  * `src/lib/storage.ts` (Cloudinary/S3 client)
* **Technologies:** Next.js API Routes, Cloudinary/AWS S3, PostgreSQL, Prisma/Drizzle.
* **Dependencies:** Milestone 1 (Requires user session to associate uploaded items with a user).
* **Testing Requirements:** Upload a test image. Verify the file exists in cloud storage and a corresponding record is created in the PostgreSQL database.

### Milestone 3: AI Processing Integration (Vision & Tagging)
* **Objective:** Automatically process uploaded images to remove backgrounds and extract clothing attributes.
* **Features:** Call Remove.bg API on upload, call OpenAI Vision API to classify the image (e.g., "Red Cotton T-Shirt", "Summer"), save attributes to DB.
* **Files/Modules Required:**
  * `src/app/api/process-image/route.ts`
  * `src/lib/ai-services.ts` (Wrappers for Remove.bg and OpenAI)
  * DB schema updates (adding color, category, style fields to Item model)
* **Technologies:** Remove.bg API, OpenAI API (gpt-4o).
* **Dependencies:** Milestone 2 (Image must be uploaded and accessible via URL).
* **Testing Requirements:** Upload an image with a complex background. Verify the saved image has a transparent background. Verify the database record contains accurate, AI-generated tags (Category, Color).

### Milestone 4: Wardrobe Organization & UI
* **Objective:** Provide a premium, dynamic UI for users to view, filter, and manage their digitized wardrobe.
* **Features:** Wardrobe gallery view, masonry or grid layout, filtering (by category/color/season), item detail view.
* **Files/Modules Required:**
  * `src/app/wardrobe/page.tsx`
  * `src/components/WardrobeGrid.tsx`
  * `src/components/FilterBar.tsx`
  * `src/components/ItemCard.tsx`
* **Technologies:** Next.js, TailwindCSS, Framer Motion (for smooth grid/filter animations).
* **Dependencies:** Milestone 3 (Requires processed, tagged images to effectively filter and display).
* **Testing Requirements:** Verify the grid renders correctly with placeholder or real data. Test all filter combinations. Ensure the UI is responsive and looks premium on mobile screens.

### Milestone 5: Intelligent Outfit Recommendations & Restyling
* **Objective:** Generate and suggest outfits based on the user's specific wardrobe items.
* **Features:** Outfit generation engine (mixing tops/bottoms/shoes), restyle suggestions, UI to view and save favorite outfits.
* **Files/Modules Required:**
  * `src/app/outfits/page.tsx`
  * `src/app/api/recommend/route.ts`
  * `src/components/OutfitCard.tsx`
  * DB schema updates (Outfit model, Item-Outfit relations)
* **Technologies:** OpenAI API (using prompt engineering to act as a stylist matching user's items) or custom rule-based heuristics.
* **Dependencies:** Milestone 4 (Requires a populated, categorized wardrobe database).
* **Testing Requirements:** Request an outfit recommendation. Verify the system returns a valid combination (e.g., Top + Bottom). Verify the UI layout for outfits is visually appealing.

## Verification Plan
1. Review this updated architecture and roadmap document.
2. Confirm the 5-milestone breakdown aligns with your expectations for the MVP.
3. Upon approval, I will generate a detailed `task.md` checklist and we can begin execution on Milestone 1.
