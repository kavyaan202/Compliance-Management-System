$(document).ready(function() {
    
    const validationRules = {
        Compliance_Details: {
            regex: /^[a-zA-Z0-9\s]{5,100}$/,
            message: "Compliance Details should be 5-100 alphanumeric characters.",
            emptyMessage: "Please fill the Compliance Details."
        },
        Name_of_Statutory: {
            regex: /^[a-zA-Z\s]{2,50}$/,
            message: "Name of Statutory should be 2-50 alphabetic characters.",
            emptyMessage: "Please fill the Name of Statutory."
        },
        Frequency: {
            required: true,
            message: "Please select a Frequency.",
            emptyMessage: "Please select a Frequency."
        },
        Document_Reference_Number: {
            regex: /^[A-Za-z0-9/ -]{5,50}(\([A-Za-z0-9 -]+\))?$/,
            message: "Document Reference Number should be 5-50 characters.",
            emptyMessage: "Please fill the Document Reference Number."
        },
        Valid_From: {
            regex: /^\d{4}-\d{2}-\d{2}$/,
            message: "Please enter a valid date in YYYY-MM-DD format.",
            emptyMessage: "Please fill the Valid From date.",
            minDate: new Date().toISOString().split('T')[0] // Today's date
        },
        Valid_Upto: {
            regex: /^\d{4}-\d{2}-\d{2}$/,
            message: "Please enter a valid date in YYYY-MM-DD format.",
            emptyMessage: "Please fill the Valid Upto date.",
            validateDate: true
        },
        Remarks: {
            regex: /^[\s\S]{10,500}$/,
            message: "Remarks should be 10-500 characters.",
            emptyMessage: "Please fill the Remarks."
        }
    };

    function validateField(field, prefix = '') {
        const value = field.val().trim();
        const name = field.attr('name');
        const rule = validationRules[name];
        const errorElement = $(`#${prefix}${name}_error`);

        // Special handling for Frequency
        if (name === 'Frequency') {
            if (!value) {
                errorElement.text(rule.emptyMessage);
                return false;
            } else {
                errorElement.text('');
                return true;
            }
        }

        // Date validation
        if (name === 'Valid_From') {
            if (value === '') {
                errorElement.text(rule.emptyMessage);
                return false;
            }
            
            const selectedDate = new Date(value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            if (selectedDate < today) {
                errorElement.text("Valid From date cannot be earlier than today.");
                return false;
            }
        }

        if (name === 'Valid_Upto') {
            if (value === '') {
                errorElement.text(rule.emptyMessage);
                return false;
            }

            // Get the correct Valid_From field based on the form
            const formId = field.closest('form').attr('id');
            const fromDate = new Date($(`#${formId} [name="Valid_From"]`).val());
            const toDate = new Date(value);

            if (toDate < fromDate) {
                errorElement.text("Valid Upto date cannot be earlier than Valid From date.");
                return false;
            }
        }

        // Regular validation for other fields
        if (value === '') {
            errorElement.text(rule.emptyMessage);
            return false;
        } else if (rule && rule.regex && !rule.regex.test(value)) {
            errorElement.text(rule.message);
            return false;
        } else {
            errorElement.text('');
            return true;
        }
    }

    function updateDateMinimums(formId) {
        const today = new Date().toISOString().split('T')[0];
        $(`#${formId} [name="Valid_From"]`).attr('min', today);
        
        const fromDate = $(`#${formId} [name="Valid_From"]`).val();
        if (fromDate) {
            $(`#${formId} [name="Valid_Upto"]`).attr('min', fromDate);
        } else {
            $(`#${formId} [name="Valid_Upto"]`).attr('min', today);
        }
    }

    function validateAllFields(formId, prefix = '') {
        let isValid = true;
        $(`#${formId} input, #${formId} textarea, #${formId} select`).each(function() {
            if (!validateField($(this), prefix)) {
                isValid = false;
            }
        });
        return isValid;
    }

    function attachValidation(formId, prefix = '') {
        // Set initial date minimums
        updateDateMinimums(formId);

        // Add change event listener for Valid_From date
        $(`#${formId} [name="Valid_From"]`).on('change', function() {
            const fromDate = $(this).val();
            if (fromDate) {
                $(`#${formId} [name="Valid_Upto"]`).attr('min', fromDate);
            }
            validateField($(this), prefix);
            // Revalidate Valid_Upto when Valid_From changes
            validateField($(`#${formId} [name="Valid_Upto"]`), prefix);
        });

        // Add change event listener for Valid_Upto date
        $(`#${formId} [name="Valid_Upto"]`).on('change', function() {
            validateField($(this), prefix);
        });

        // Existing validation
        $(`#${formId} select`).on('change', function() {
            validateField($(this), prefix);
        });

        $(`#${formId} input, #${formId} textarea`).on('input', function() {
            validateField($(this), prefix);
        });

        $(`#${formId}`).on('submit', function(e) {
            e.preventDefault();
            if (validateAllFields(formId, prefix)) {
                this.submit();
            }
        });
    }
    

    // Attach validation to both forms
    attachValidation('complianceForm');
    attachValidation('editComplianceForm', 'edit');
});