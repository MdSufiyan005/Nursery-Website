document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('checkoutForm');

    form?.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const phone = formData.get('phone_number');
        const pincode = formData.get('pincode');

        if (!/^\d{10}$/.test(phone)) {
            alert('Please enter a valid 10-digit phone number');
            return;
        }

        if (!/^\d{6}$/.test(pincode)) {
            alert('Please enter a valid 6-digit pincode');
            return;
        }

        const submitButton = document.getElementById('paymentButton');
        submitButton.disabled = true;
        submitButton.innerHTML = '⏳ Processing...';

        try {
            form.submit();
        } catch (error) {
            console.error('Error:', error);
            alert('Something went wrong. Please try again.');
            submitButton.disabled = false;
            submitButton.innerHTML = '💳 Proceed to Payment';
        }
    });

    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('change', async (e) => {
            const row = e.target.closest('tr');
            const plantId = row.dataset.plantId;
            const quantity = parseInt(e.target.value);

            if (quantity < 1) {
                e.target.value = 1;
                return;
            }

            const formData = new FormData();
            formData.append('quantity', quantity);

            try {
                const response = await fetch(`/update-cart-quantity/${plantId}/`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                });

                if (response.ok) {
                    window.location.reload();
                }
            } catch (err) {
                console.error('Failed to update quantity:', err);
            }
        });
    });

    document.querySelectorAll('.remove-item').forEach(button => {
        button.addEventListener('click', async (e) => {
            const plantId = e.target.dataset.plantId;
            try {
                const response = await fetch(`/remove-from-cart/${plantId}/`);
                if (response.ok) {
                    window.location.reload();
                }
            } catch (err) {
                console.error('Failed to remove item:', err);
            }
        });
    });
});