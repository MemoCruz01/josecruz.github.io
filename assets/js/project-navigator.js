/**
 * Project Navigator - Auto-injects elegant project navigation
 * Scales seamlessly as new projects are added
 */

const PROJECTS = [
  {
    id: 1,
    name: "Autonomous Guided Vehicle",
    category: "Robotics",
    slug: "project-1-agv",
    icon: "robot"
  },
  {
    id: 2,
    name: "Electric Vehicle Assembly",
    category: "Automation",
    slug: "project-2-ev-assembly",
    icon: "hammer"
  },
  {
    id: 3,
    name: "BMW Robotic Cell",
    category: "AI & Optimization",
    slug: "project-3-bmw-cell",
    icon: "cpu"
  },
  {
    id: 4,
    name: "BAJA SAE Vehicle",
    category: "Automotive",
    slug: "project-4-baja",
    icon: "car-front"
  },
  {
    id: 5,
    name: "ROS Navigation",
    category: "Robotics",
    slug: "project-5-ros-navigation",
    icon: "diagram-3"
  },
  {
    id: 6,
    name: "Gesture Recognition",
    category: "Computer Vision",
    slug: "project-6-gesture-recognition",
    icon: "hand-index"
  },
  {
    id: 7,
    name: "Swarm Robotics",
    category: "Multi-Robot Systems",
    slug: "Project-7-swarm-robotic-path-planning_n_exploration",
    path: "Project-7-swarm-robotic-path-planning_n_exploration/project-7-swarm",
    icon: "bezier"
  },
  {
    id: 8,
    name: "Harvesting System",
    category: "Autonomous Systems",
    slug: "project-8-harvesting",
    path: "project-8-harvesting-system/project-8-harvesting",
    icon: "gear"
  }
];

// Detect current project from URL
function getCurrentProjectId() {
  const pathname = window.location.pathname;
  for (let project of PROJECTS) {
    if (pathname.includes(project.slug)) {
      return project.id;
    }
  }
  return null;
}

// Build project navigator HTML
function buildProjectNavigator() {
  const currentId = getCurrentProjectId();
  if (!currentId) return; // Not on a project page

  const currentProject = PROJECTS.find(p => p.id === currentId);
  const previousProject = PROJECTS.find(p => p.id === currentId - 1);
  const nextProject = PROJECTS.find(p => p.id === currentId + 1);

  const previousLink = previousProject
    ? `../../projects/${previousProject.path || previousProject.slug + "/" + previousProject.slug}.html`
    : "#";
  const nextLink = nextProject
    ? `../../projects/${nextProject.path || nextProject.slug + "/" + nextProject.slug}.html`
    : "#";

  const previousDisabled = !previousProject ? "disabled" : "";
  const nextDisabled = !nextProject ? "disabled" : "";

  const html = `
    <div class="project-navigator" role="navigation" aria-label="Project navigation">
      <div class="navigator-container">
        <!-- Left Navigation (Previous Button) -->
        <div class="nav-left">
          <a href="${previousLink}" class="nav-button prev-button ${previousDisabled}" 
             ${previousDisabled ? 'tabindex="-1" aria-disabled="true"' : ''} title="Go to previous project">
            <i class="bi bi-chevron-left"></i>
            <span class="nav-label">${previousProject ? previousProject.name : 'Previous'}</span>
          </a>
        </div>

        <!-- Center Navigation (Info) -->
        <div class="nav-center-section">
          <div class="project-counter">
            <span class="current">${currentId}</span>
            <span class="separator">/</span>
            <span class="total">${PROJECTS.length}</span>
          </div>
          <div class="project-info">
            <p class="project-name">${currentProject.name}</p>
            <p class="project-category">${currentProject.category}</p>
          </div>
        </div>

        <!-- Right Navigation (Next Button + All Projects) -->
        <div class="nav-right">
          <a href="${nextLink}" class="nav-button next-button ${nextDisabled}"
             ${nextDisabled ? 'tabindex="-1" aria-disabled="true"' : ''} title="Go to next project">
            <span class="nav-label">${nextProject ? nextProject.name : 'Next'}</span>
            <i class="bi bi-chevron-right"></i>
          </a>
          <a href="../../portfolio-details.html" class="nav-button all-projects-button" title="View all projects">
            <i class="bi bi-grid-3x3-gap"></i>
            <span>All Projects</span>
          </a>
        </div>
      </div>

      <!-- Visual Progress Bar -->
      <div class="progress-bar">
        <div class="progress-fill" style="width: ${(currentId / PROJECTS.length) * 100}%"></div>
      </div>
    </div>
  `;

  // Insert after header
  const header = document.querySelector("header");
  if (header) {
    header.insertAdjacentHTML("afterend", html);
  } else {
    document.body.insertAdjacentHTML("afterbegin", html);
  }

  // Setup keyboard navigation
  setupKeyboardNavigation(previousLink, nextLink, previousDisabled, nextDisabled);
}

// Keyboard shortcuts
function setupKeyboardNavigation(prevLink, nextLink, prevDisabled, nextDisabled) {
  document.addEventListener("keydown", function(e) {
    if (e.key === "ArrowLeft" && !prevDisabled) {
      window.location.href = prevLink;
    } else if (e.key === "ArrowRight" && !nextDisabled) {
      window.location.href = nextLink;
    }
  });
}

// Initialize when DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", buildProjectNavigator);
} else {
  buildProjectNavigator();
}
