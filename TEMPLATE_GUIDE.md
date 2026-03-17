# Portfolio Template Structure Guide

## 📁 Project Overview

This is a **Bootstrap-based portfolio template** with a dark theme. It's structured to be modular and easy to customize. Here's how everything is organized:

```
josecruz.github.io/
├── index.html                 # Main webpage (all sections here)
├── portfolio-details.html     # Individual portfolio project page
├── service-details.html       # Individual service details page
├── starter-page.html          # Blank template for new pages
├── assets/
│   ├── css/
│   │   └── main.css          # All styling (colors, layouts, sections)
│   ├── js/
│   │   └── main.js           # Interactive features (scrolling, animations)
│   ├── img/                  # All images organized by category
│   │   ├── person/           # People photos
│   │   ├── portfolio/        # Project images
│   │   ├── profile/          # Your profile pictures
│   │   └── services/         # Service icons/images
│   ├── vendor/               # External libraries (Bootstrap, Swiper, etc.)
│   └── scss/                 # Source files for CSS (if compiling)
└── forms/
    └── contact.php           # Backend for contact form

```

---

## 🎨 How the Template Works

### **1. HTML Structure (index.html)**
The page is divided into **sections** that appear one after another:

```html
<section id="hero" class="hero section">
  <!-- Hero/intro section -->
</section>

<section id="about" class="about section">
  <!-- About you section -->
</section>

<section id="resume" class="resume section">
  <!-- Education & Experience -->
</section>

<section id="portfolio" class="portfolio section">
  <!-- Your projects -->
</section>

<section id="services" class="services section">
  <!-- What you offer -->
</section>

<section id="testimonials" class="testimonials section">
  <!-- Client feedback -->
</section>

<section id="opportunities" class="opportunities section">
  <!-- NEW: Your ETH Zurich application -->
</section>

<section id="contact" class="contact section">
  <!-- Contact form -->
</section>
```

**Key Pattern:**
- Each section has an `id` (used for navigation links)
- Class `section` applies common styling
- Content is wrapped in Bootstrap's `.container` for responsive layout
- `.row` and `.col-` classes handle responsive grid layout

### **2. CSS Organization (main.css)**

The CSS file has clear sections marked with comments:

```css
/*--------------------------------------------------------------
# Font & Color Variables
--------------------------------------------------------------*/
:root {
  --accent-color: #22e7a1;        /* Your brand green */
  --background-color: #25303f;    /* Dark background */
  --default-color: #f3f4f6;       /* Light text */
  --heading-color: #f9fafb;       /* Brightest text */
}

/*--------------------------------------------------------------
# Hero Section
--------------------------------------------------------------*/
.hero { ... }

/*--------------------------------------------------------------
# About Section
--------------------------------------------------------------*/
.about { ... }

/*--------------------------------------------------------------
# Services Section
--------------------------------------------------------------*/
.services { ... }
```

**How to customize colors:**
Simply change the CSS variables at the top of `main.css` and it updates the entire site!

---

## 🔧 Common Modifications Guide

### **A. Change Colors**
Edit the CSS variables in `main.css` (lines ~22-32):

```css
:root {
  --accent-color: #22e7a1;        /* Change this to your brand color */
  --background-color: #25303f;    /* Background */
  --default-color: #f3f4f6;       /* Regular text */
  --heading-color: #f9fafb;       /* Headings */
  --surface-color: #293443;       /* Card backgrounds */
}
```

### **B. Change Text Content**
In `index.html`, find the section and update the text directly:

```html
<h1>Your New Title Here</h1>
<p>Your description goes here</p>
```

**Example:** To change your name in the hero section:
```html
<!-- Find this -->
<h1 data-aos="fade-up" data-aos-delay="200">
  Creative Leader Technologist
  <span class="accent-text">Enthusiast Innovator</span>
</h1>

<!-- Change to -->
<h1 data-aos="fade-up" data-aos-delay="200">
  Your Message Here
  <span class="accent-text">Your Subtitle</span>
</h1>
```

### **C. Update Images**
1. Add your image to `assets/img/` in the appropriate folder
2. Update the `src` path in HTML:

```html
<!-- Change this -->
<img src="assets/img/profile/profile-square-14.webp" alt="">

<!-- To your image -->
<img src="assets/img/profile/your-image.jpg" alt="">
```

### **D. Add New Portfolio Projects**
In the Portfolio section, copy this block and modify:

```html
<div class="col-lg-6 portfolio-item isotope-item filter-branding">
  <div class="portfolio-card">
    <div class="portfolio-image">
      <img src="assets/img/portfolio/YOUR-IMAGE.webp" class="img-fluid" alt="Project Name">
    </div>
    <div class="portfolio-content">
      <div class="portfolio-meta">
        <span class="portfolio-category">Your Category</span>
        <span class="portfolio-year">2025</span>
      </div>
      <h3 class="portfolio-title">Your Project Name</h3>
      <p class="portfolio-description">Project description.</p>
    </div>
  </div>
</div>
```

### **E. Add New Skills**
In the Skills section, add skills like this:

```html
<div class="skill-row">
  <div class="skill-info">
    <span class="skill-name">Your Skill Name</span>
    <span class="skill-percentage">85%</span>
  </div>
  <div class="progress">
    <div class="progress-bar" role="progressbar" aria-valuenow="85" aria-valuemin="0" aria-valuemax="100"></div>
  </div>
</div>
```

### **F. Update Resume/Experience**
Find the experience timeline and update:

```html
<div class="timeline-item">
  <div class="timeline-dot"></div>
  <div class="timeline-content">
    <div class="position-meta">
      <span class="timeline-year">2025 - Present</span>
    </div>
    <h3>Your Job Title</h3>
    <h4>Your Company</h4>
    <p>Job description here.</p>
  </div>
</div>
```

---

## 🎯 Special Features Explained

### **1. Animations (data-aos)**
The template uses AOS (Animate On Scroll) library for animations:

```html
<div data-aos="fade-up" data-aos-delay="200">
  Content appears faded up when scrolling
</div>
```

**Common animations:**
- `fade-up` - Fades in from bottom
- `fade-down` - Fades in from top
- `fade-left` / `fade-right` - Fades from sides
- `zoom-in` - Zooms into view
- `slide-up` / `slide-down` - Slides in

**Delay options:** `data-aos-delay="100"` (in milliseconds)

### **2. Bootstrap Grid System**
```html
<div class="container">
  <div class="row">
    <div class="col-lg-6">  <!-- 50% width on large screens -->
      Left column
    </div>
    <div class="col-lg-6">
      Right column
    </div>
  </div>
</div>
```

**Common column sizes:**
- `col-lg-6` = 50% width (2 columns)
- `col-lg-4` = 33% width (3 columns)
- `col-lg-3` = 25% width (4 columns)
- On mobile (small screens), automatically stacks to full width

### **3. Icons (Bootstrap Icons)**
```html
<i class="bi bi-house"></i>           <!-- Home -->
<i class="bi bi-person"></i>          <!-- Person -->
<i class="bi bi-file-earmark"></i>    <!-- Document -->
<i class="bi bi-palette"></i>         <!-- Palette -->
<i class="bi bi-code-slash"></i>      <!-- Code -->
<i class="bi bi-star-fill"></i>       <!-- Star -->
```

See all icons at: https://icons.getbootstrap.com/

---

## 🚀 Modification Workflow

Here's your step-by-step process for making changes:

### **To Change Text:**
1. Open `index.html` in VS Code
2. Find the section (use Ctrl+F to search)
3. Locate the text you want to change
4. Update it
5. Save (Ctrl+S)
6. Refresh your browser

### **To Change Styling:**
1. Open `assets/css/main.css`
2. Search for the section name (e.g., `.hero`, `.about`)
3. Find the property you want to change
4. Modify it
5. Save and refresh browser

### **To Add New Sections:**
1. Copy an existing section in `index.html`
2. Change the `id` attribute
3. Update the content
4. Add navigation link in the header
5. Add CSS styles in `main.css`

---

## 📋 Important Files Reference

| File | Purpose | When to Edit |
|------|---------|-------------|
| `index.html` | All page content | Text, sections, layout, images |
| `assets/css/main.css` | All styling | Colors, fonts, spacing, animations |
| `assets/js/main.js` | Interactive features | If you need custom JavaScript |
| `assets/img/` | Images | Add/replace your pictures here |
| `forms/contact.php` | Contact form backend | If contact form isn't working |

---

## 💡 Quick Tips

✅ **Always:**
- Keep backups of working versions
- Make one change at a time
- Test in browser after each change
- Use meaningful filenames for images

❌ **Avoid:**
- Deleting closing tags (`</div>`, `</section>`)
- Changing class names without checking CSS
- Using special characters in filenames
- Directly modifying vendor files

---

## 🎓 Next Steps

1. **Explore** - Open files and see how they work together
2. **Experiment** - Try small changes (colors, text, images)
3. **Document** - Keep notes of what works
4. **Build** - Gradually customize it to match your portfolio

Questions? Look for the pattern in existing code and replicate it for your new content!
