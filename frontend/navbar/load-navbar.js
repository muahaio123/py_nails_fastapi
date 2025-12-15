// Function to load navbar component and set active nav item
function loadNavbar(activePage) {
    fetch('../navbar/navbar-component.html?v=3')
        .then(response => response.text())
        .then(html => {
            // Insert navbar at the beginning of the body
            const navContainer = document.createElement('div');
            navContainer.id = 'navbar-container';
            navContainer.innerHTML = html;
            document.body.insertBefore(navContainer, document.body.firstChild);
            
            // Load the new work offcanvas component, pass the active page so component can adapt
            loadNewWorkComponent(activePage);
            
            // Set the active nav item with styling
            if (activePage === 'home') {
                const homeNav = document.getElementById('homeNav');
                if (homeNav) {
                    const link = homeNav.querySelector('a');
                    if (link) {
                        link.classList.add('active');
                        link.style.backgroundColor = 'rgba(52, 152, 219, 0.8)';
                        link.style.color = '#fff !important';
                    }
                }
            } else if (activePage === 'work') {
                const workNav = document.getElementById('workNav');
                if (workNav) {
                    const link = workNav.querySelector('a');
                    if (link) {
                        link.classList.add('active');
                        link.style.backgroundColor = 'rgba(52, 152, 219, 0.8)';
                        link.style.color = '#fff !important';
                    }
                }
            } else if (activePage === 'employee') {
                const employeeNav = document.getElementById('employeeNav');
                if (employeeNav) {
                    const link = employeeNav.querySelector('a');
                    if (link) {
                        link.classList.add('active');
                        link.style.backgroundColor = 'rgba(52, 152, 219, 0.8)';
                        link.style.color = '#fff !important';
                    }
                }
            }
            
            // Add hover effects to nav links
            const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
            navLinks.forEach(link => {
                link.addEventListener('mouseenter', function() {
                    if (!this.classList.contains('active')) {
                        this.style.backgroundColor = 'rgba(149, 165, 166, 0.4)';
                    }
                });
                link.addEventListener('mouseleave', function() {
                    if (!this.classList.contains('active')) {
                        this.style.backgroundColor = 'transparent';
                    }
                });
            });
            
            // Add hover effects to button
            const newWorkBtn = document.getElementById('newWorkBtn');
            if (newWorkBtn) {
                newWorkBtn.addEventListener('mouseenter', function() {
                    this.style.transform = 'translateY(-2px)';
                    this.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.2)';
                });
                newWorkBtn.addEventListener('mouseleave', function() {
                    this.style.transform = 'translateY(0)';
                    this.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.15)';
                });
            }
        })
        .catch(error => console.error('Error loading navbar:', error));
}

// Function to load new work offcanvas component
function loadNewWorkComponent(sourcePage) {
    fetch('../newwork/newwork-offcanvas.html?v=1')
        .then(response => response.text())
        .then(html => {
            // Insert the component at the end of body
            const container = document.createElement('div');
            container.innerHTML = html;
            document.body.appendChild(container);

            // Add a source-specific class to the offcanvas for page-specific styling (e.g., source-home)
            try {
                if (sourcePage) {
                    const offcanvasEl = document.getElementById('newWorkOffcanvas');
                    if (offcanvasEl) {
                        offcanvasEl.classList.add(`source-${sourcePage}`);
                    }
                }
            } catch (err) {
                // ignore if element not present yet
            }

            // Load the JavaScript file for newwork component
            const script = document.createElement('script');
            script.src = '../newwork/newwork-offcanvas.js?v=1';
            script.type = 'text/javascript';
            script.onload = function() {
                // Initialize the offcanvas after script loads
                try {
                    initializeOffcanvas();
                } catch (err) {
                    console.error('initializeOffcanvas threw:', err);
                }
            };
            document.body.appendChild(script);
        })
        .catch(error => console.error('Error loading new work component:', error));
}

// Function to initialize offcanvas
function initializeOffcanvas() {
    // Prefer the centralized initializer from newwork-offcanvas if available
    if (window.initializeNewWorkOffcanvas) {
        try {
            window.initializeNewWorkOffcanvas();
        } catch (err) {
            console.error('window.initializeNewWorkOffcanvas threw:', err);
        }
        return;
    }

    var workOffcanvas = document.getElementById("newWorkOffcanvas");
    var workBtn = document.getElementById("newWorkBtn");

    // When the user clicks the button, open the offcanvas using Bootstrap
    if (workBtn && workOffcanvas) {
        workBtn.onclick = function() {
            const offcanvas = new bootstrap.Offcanvas(workOffcanvas);
            offcanvas.show();
            // Set default datetime when offcanvas opens
            setDefaultDateTimeOffcanvas();
            loadEmployeesOffcanvas();
        }
    }
    
    // Setup form and button handlers (fallback)
    setupNewWorkForm();
}

// Set default datetime to current system time for offcanvas
function setDefaultDateTimeOffcanvas() {
    const datetimeInput = document.getElementById("work_datetime_offcanvas");
    if (datetimeInput) {
        const now = new Date();
        // Format: YYYY-MM-DDTHH:mm
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        
        datetimeInput.value = `${year}-${month}-${day}T${hours}:${minutes}`;
    }
}

// Load employees for offcanvas form
function loadEmployeesOffcanvas() {
    // Delegate to newwork-offcanvas if available
    if (window.loadEmployeesOffcanvas) return window.loadEmployeesOffcanvas();
}

// Add employee work item
function addEmployeeWorkItem() {
    if (window.addEmployeeWorkItem) return window.addEmployeeWorkItem();
}

// Setup event listeners for a work item
function setupItemEventListeners(itemId) {
    if (window.setupItemEventListeners) return window.setupItemEventListeners(itemId);
}

// Remove employee work item
function removeEmployeeWorkItem(itemId) {
    if (window.removeEmployeeWorkItem) return window.removeEmployeeWorkItem(itemId);
}

// Update totals display
function updateTotals() {
    if (window.updateTotals) return window.updateTotals();
}

// Clear form to brand new state
function clearNewWorkForm() {
    if (window.clearNewWorkForm) return window.clearNewWorkForm();
}

// Setup new work form handlers
function setupNewWorkForm() {
    // Delegate entire form setup/handlers to the new work component if available
    if (window.initializeNewWorkOffcanvas) return;
}
