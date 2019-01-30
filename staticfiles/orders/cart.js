// Compile template for cart item
const template = Handlebars.compile(document.querySelector('#cart-template').innerHTML);

// Register handlebars helper for displaying extras in cart
Handlebars.registerHelper('extra', function(extra) {
    out = extra.name;
    if (extra.hasCost == "true")
        out += ` (+${extra.cost})`;
    return out;
});

// Get cart info from localStorage
const cart = JSON.parse(localStorage.getItem('cart'));

document.addEventListener('DOMContentLoaded', () => {

    // Display cart items
    const itemList = document.querySelector('#items');
    console.log(cart);
    itemList.innerHTML = template({'cart': cart});

    // Display cart total and submit button
    if (cart) {
        document.querySelector('#submit').style.display = 'block';

        // Calculate and display total
        let total = 0;
        cart.forEach(item => total += Number.parseFloat(item.price));
        const totalElement = document.querySelector('#total');
        totalElement.innerHTML += '$' + `${total.toFixed(2)}`;
        totalElement.style.display = 'block';
    }

    // Submit the order
    document.querySelector('#submit').onclick = () => {

        const request = new XMLHttpRequest();
        request.open('POST', 'cart/submit-order');

        // Callback for when request completes
        request.onload = () => {
            const response = JSON.parse(request.responseText);
            console.log(response);
            if (response.success) {
                alert('Order Submitted!');
                order_success();

            }
            else {
                alert('something went wrong');
            }
        };

        // Attach CSRF token to AJAX request
        const csrf = Cookies.get('csrftoken');
        request.setRequestHeader('X-CSRFToken', csrf);

        // Add cart to request data
        const data = new FormData();
        const cartString = JSON.stringify(cart);
        data.append('cart', cartString);

        //Send AJAX request
        request.send(data);

    };

});

function order_success() {

    // Empty cart from localStorage
    localStorage.removeItem('cart');

    // Remove submit button
    document.querySelector('#submit').style.display = 'none';

    // Remove total
    document.querySelector('#total').style.display = 'none';

    // Reset cart
    rendered = template();
    console.log(rendered);
    document.querySelector('#items').innerHTML = template();
    console.log(document.querySelector('#items').innerHTML);

}
