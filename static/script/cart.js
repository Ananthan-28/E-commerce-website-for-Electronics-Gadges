function updateQuantity(productId, direction) {
  const numberInput = document.getElementById(`number${productId}`);
  const quantity = parseInt(numberInput.value);

  if (direction === 'increment' && quantity < 999) { // Limit to a high value (adjust as needed)
    numberInput.value = quantity + 1;
  } else if (direction === 'decrement' && quantity > 1) {
    numberInput.value = quantity - 1;
  }

  // Update decrement button state based on new quantity
  document.getElementById(`decrement${productId}`).disabled = quantity === 1;
}

function increment(productId) {
  updateQuantity(productId, 'increment');
}

function decrement(productId) {
  updateQuantity(productId, 'decrement');
}

window.onload = function() {
  const numberInputs = document.querySelectorAll('.form-control.text-center');
  for (const input of numberInputs) {
    const productId = parseInt(input.id.replace('number', ''));
    if (parseInt(input.value) === 1) {
      document.getElementById(`decrement${productId}`).disabled = true;
    }
  }
}

function checkInput() {
    var searchData = document.getElementById('searchData').value;
    if (searchData.trim() !== '') {
        document.getElementById('submitButton').disabled = false;
    } else {
        document.getElementById('submitButton').disabled = true;
    }
}