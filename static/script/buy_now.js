function increment() {
  let number = document.getElementById('number');
  number.value = parseInt(number.value) + 1;
  document.getElementById('decrement').disabled = false;
}

function decrement() {
  let number = document.getElementById('number');
  if (parseInt(number.value) > 1) {
    number.value = parseInt(number.value) - 1;
  }
  if (parseInt(number.value) === 1) {
    document.getElementById('decrement').disabled = true;
  }
}

window.onload = function() {
  if (parseInt(document.getElementById('number').value) === 1) {
    document.getElementById('decrement').disabled = true;
  }
}
const payment_method = document.querySelectorAll('input[name="payment_method"]');
const payment_forms = document.querySelectorAll('.payment-form');

payment_method.forEach(radio => {
  radio.addEventListener('click', function() {
    payment_forms.forEach(form => {
      form.classList.add('d-none');
    });
    const selected_form_id = `#${this.id}_form`;
    const selected_form = document.querySelector(selected_form_id);
    if (selected_form) {
      selected_form.classList.remove('d-none');
    }
  });
});

window.addEventListener("DOMContentLoaded", function() {
  const payment_methods = document.querySelectorAll('input[type="radio"][name="payment_method"]');
  payment_methods.forEach(radio => radio.checked = false);
});

const creditCardMonthSelect = document.getElementById("valid_cc_month");
const creditCardYearSelect = document.getElementById("valid_cc_year");
const creditCardExpiryInput = document.getElementById("valid_cc");

// Debit Card Expiry Elements (already defined previously)
const debitCardMonthSelect = document.getElementById("valid_dc_month");
const debitCardYearSelect = document.getElementById("valid_dc_year");
const debitCardExpiryInput = document.getElementById("valid_dc");

function populateYears() {
  const currentYear = new Date().getFullYear();
  const yearsToShow = 10;

  for (let year = currentYear; year <= currentYear + yearsToShow; year++) {
    const option = document.createElement("option");
    option.text = year;
    option.value = year;
    creditCardYearSelect.appendChild(option);
    debitCardYearSelect.appendChild(option); // Add year options to both debit and credit card selects
  }
}

function updateExpiryValue() {
  // Check for credit card selection (assuming selection is based on radio button with ID "credit_card")
  if (document.getElementById("credit_card").checked) {
    const selectedMonth = creditCardMonthSelect.value;
    const selectedYear = creditCardYearSelect.value;
    
    if (selectedMonth && selectedYear) {
      const expiryValue = `${selectedYear}-${selectedMonth.padStart(2, "0")}`;
      creditCardExpiryInput.value = expiryValue;
    } else {
      creditCardExpiryInput.value = "";
    }
  } else { // Code for debit card expiry remains the same (already defined previously)
    const selectedMonth = debitCardMonthSelect.value;
    const selectedYear = debitCardYearSelect.value;
    
    if (selectedMonth && selectedYear) {
      const expiryValue = `${selectedYear}-${selectedMonth.padStart(2, "0")}`;
      debitCardExpiryInput.value = expiryValue;
    } else {
      debitCardExpiryInput.value = "";
    }
  }
}

populateYears();
creditCardMonthSelect.addEventListener("change", updateExpiryValue);
creditCardYearSelect.addEventListener("change", updateExpiryValue);
// Existing listeners for debit card expiry remain (not shown here for brevity)