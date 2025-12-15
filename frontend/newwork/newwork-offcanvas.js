let employeesList = [];
let workItems = [];

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
    // Add hardcoded employees (you can replace this with API call)
    employeesList = [
        { id: 1, name: "Long" },
        { id: 2, name: "Soc" }
    ];
}

// Add employee work item
function addEmployeeWorkItem() {
    const container = document.getElementById("employeeWorkItemsContainer");
    const itemId = Date.now();
    
    const itemHTML = `
        <div class="employee-work-item" data-item-id="${itemId}" style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #3498db;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h6 style="margin: 0;">Employee Work</h6>
                <button type="button" class="btn btn-sm btn-outline-danger remove-item-btn" data-item-id="${itemId}">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
            
            <!-- Employee Selection -->
            <div style="margin-bottom: 1rem;">
                <label class="form-label" style="font-size: 0.9rem;">
                    <i class="bi bi-person"></i> Employee
                </label>
                <select class="form-select employee-select" data-item-id="${itemId}">
                    <option value="">Select employee...</option>
                </select>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <!-- Amount -->
                <div>
                    <label class="form-label" style="font-size: 0.9rem;">
                        <i class="bi bi-cash-coin"></i> Amount ($)
                    </label>
                    <input type="number" class="form-control work-amount" data-item-id="${itemId}" step="1" min="0" value="0">
                </div>
                
                <!-- Tip -->
                <div>
                    <label class="form-label" style="font-size: 0.9rem;">
                        <i class="bi bi-gift"></i> Tip ($)
                    </label>
                    <input type="number" class="form-control work-tip" data-item-id="${itemId}" step="1" min="0" value="0">
                </div>
            </div>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', itemHTML);
    
    // Populate employee dropdown
    const employeeSelect = document.querySelector(`[data-item-id="${itemId}"].employee-select`);
    employeesList.forEach(emp => {
        const option = document.createElement("option");
        option.value = emp.id;
        option.textContent = emp.name;
        employeeSelect.appendChild(option);
    });
    
    // Add event listeners
    setupItemEventListeners(itemId);
}

// Setup event listeners for a work item
function setupItemEventListeners(itemId) {
    const removeBtn = document.querySelector(`[data-item-id="${itemId}"].remove-item-btn`);
    const amountInput = document.querySelector(`[data-item-id="${itemId}"].work-amount`);
    const tipInput = document.querySelector(`[data-item-id="${itemId}"].work-tip`);
    
    if (removeBtn) {
        removeBtn.addEventListener('click', function() {
            removeEmployeeWorkItem(itemId);
        });
    }
    
    if (amountInput) {
        amountInput.addEventListener('change', updateTotals);
    }
    
    if (tipInput) {
        tipInput.addEventListener('change', updateTotals);
    }
}

// Remove employee work item
function removeEmployeeWorkItem(itemId) {
    const item = document.querySelector(`[data-item-id="${itemId}"]`);
    if (item) {
        item.remove();
        updateTotals();
    }
}

// Update totals
function updateTotals() {
    let totalAmount = 0;
    let totalTips = 0;
    
    document.querySelectorAll('.employee-work-item').forEach(item => {
        const amountInput = item.querySelector('.work-amount');
        const tipInput = item.querySelector('.work-tip');
        
        if (amountInput) {
            totalAmount += parseFloat(amountInput.value) || 0;
        }
        if (tipInput) {
            totalTips += parseFloat(tipInput.value) || 0;
        }
    });
    
    const discount = parseFloat(document.getElementById("work_discount_offcanvas").value) || 0;
    const grandTotal = totalAmount + totalTips - discount;
    
    document.getElementById("totalAmount").textContent = totalAmount.toFixed(2);
    document.getElementById("totalTips").textContent = totalTips.toFixed(2);
    document.getElementById("grandTotal").textContent = grandTotal.toFixed(2);
}

// Clear form to brand new state
function clearNewWorkForm() {
    const form = document.getElementById("newWorkFormOffcanvas");
    if (form) {
        form.reset();
        // Clear all work items
        document.getElementById("employeeWorkItemsContainer").innerHTML = '';
        workItems = [];
        // Reset datetime to current time
        setDefaultDateTimeOffcanvas();
        // Reset totals
        updateTotals();
    }
}

// Initialize the new work offcanvas component
function initializeNewWorkOffcanvas() {
    const cancelBtn = document.getElementById("cancelBtnOffcanvas");
    const addEmployeeBtn = document.getElementById("addEmployeeBtn");
    const form = document.getElementById("newWorkFormOffcanvas");
    const offcanvas = document.getElementById("newWorkOffcanvas");
    const discountInput = document.getElementById("work_discount_offcanvas");
    
    // Handle add employee button
    if (addEmployeeBtn) {
        addEmployeeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            addEmployeeWorkItem();
        });
    }
    
    // Handle discount changes
    if (discountInput) {
        discountInput.addEventListener('change', updateTotals);
    }
    
    // Handle cancel button - clear form and close
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            clearNewWorkForm();
            const bsOffcanvas = bootstrap.Offcanvas.getInstance(offcanvas);
            if (bsOffcanvas) {
                bsOffcanvas.hide();
            }
        });
    }
    
    // Handle form submission
    if (form) {
        form.addEventListener("submit", function(e) {
            e.preventDefault();
            // Collect all work items data
            const workData = {
                datetime: document.getElementById("work_datetime_offcanvas").value,
                discount: parseFloat(document.getElementById("work_discount_offcanvas").value) || 0,
                notes: document.getElementById("work_notes_offcanvas").value,
                items: []
            };
            
            document.querySelectorAll('.employee-work-item').forEach(item => {
                const itemId = item.getAttribute('data-item-id');
                workData.items.push({
                    employee_id: item.querySelector('.employee-select').value,
                    amount: parseFloat(item.querySelector('.work-amount').value) || 0,
                    tip: parseFloat(item.querySelector('.work-tip').value) || 0
                });
            });
            
            // Submission handler - TODO: send to backend API
            // TODO: Send workData to backend API
            
            // Close offcanvas after submission
            const bsOffcanvas = bootstrap.Offcanvas.getInstance(offcanvas);
            if (bsOffcanvas) {
                bsOffcanvas.hide();
            }
            // Clear form for next entry
            clearNewWorkForm();
        });
    }
    
    // When offcanvas is shown, set defaults and load employees
    if (offcanvas) {
        offcanvas.addEventListener('show.bs.offcanvas', function() {
            setDefaultDateTimeOffcanvas();
            loadEmployeesOffcanvas();
        });
    }

    // Ensure navbar button opens the offcanvas
    const workBtn = document.getElementById("newWorkBtn");
    if (workBtn && offcanvas) {
        workBtn.addEventListener('click', function() {
            const bsOffcanvas = new bootstrap.Offcanvas(offcanvas);
            bsOffcanvas.show();
        });
    }
}

// Expose functions to global scope for use by the navbar loader
window.initializeNewWorkOffcanvas = initializeNewWorkOffcanvas;
window.clearNewWorkForm = clearNewWorkForm;
window.setDefaultDateTimeOffcanvas = setDefaultDateTimeOffcanvas;
window.loadEmployeesOffcanvas = loadEmployeesOffcanvas;
window.addEmployeeWorkItem = addEmployeeWorkItem;
window.updateTotals = updateTotals;

