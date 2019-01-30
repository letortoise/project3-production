const optionsTemplate = Handlebars.compile(document.querySelector('#options-template').innerHTML);

document.addEventListener('DOMContentLoaded', () => {
    // For simplicity, create an interface for interacting with the modal window
    const modalWindow = {
        title: document.querySelector('#modalTitle'),
        submitButton: document.querySelector('#submit'),
        body: document.querySelector('#modalBody'),
        sizeButtons: document.querySelector('#size'),
        extras: document.querySelector('#extras')
    };

    // When user selects a menu item, open modal window for order customization
    const items = document.querySelectorAll('.menu-item');
    items.forEach(item => {
        item.onclick = () => {
            prepareModal(item, modalWindow);
            $('#optionsModal').modal('toggle');
        };
    });
});

// When user selects an item, populate modal window with the information for that item
function prepareModal(item, modalWindow) {

    // Get item info
    const id = item.dataset.pk;
    const name = item.dataset.name;
    const isOneSize = (item.dataset.isOneSize == "True");
    const takesExtras = (item.dataset.takesExtras == "True");
    const numberToppings = item.dataset.numberToppings;
    let price = item.dataset.price;
    let size;
    let extras;

    // Set window title
    modalWindow.title.innerHTML = name;

    // Reset body
    modalWindow.sizeButtons.style.display = 'none';
    modalWindow.extras.innerHTML = '';
    modalWindow.body.style.display = 'none';

    // Display size options if the item takes multiple sizes
    if (!isOneSize) {
        modalWindow.sizeButtons.style.display = 'flex';
        modalWindow.body.style.display = 'block';
    }

    // Display extras options if the item takes extras
    if (takesExtras) {
        const extras = JSON.parse(item.dataset.extras);
        template = optionsTemplate({'extras': extras});
        modalWindow.extras.innerHTML = template;
        modalWindow.extras.style.display = 'block';
    }

    // When user clicks submit, add item to cart, then close window
    const submit = document.querySelector('#submit');
    submit.onclick = () => {

        // Make sure user has selected a size if required
        const sizeSelection = document.querySelector('input[name=size]:checked');
        if (!isOneSize) {
            if (sizeSelection)
                size = sizeSelection.dataset.value;
            else {
                alert('you must choose a size');
                return;
            }
        }

        // Get extras selections from modal window
        const extrasElements = document.querySelectorAll('input[name=extra]:checked');
        if (extrasElements.length > 0) {
            // Make sure user has selected extras, if item requries (ex. 2 topping pizza)
            if (numberToppings) {
                if (numberToppings != extrasElements.length) {
                    alert(`you must choose ${numberToppings} toppings`);
                    return;
                }
            }
            // Get extras
            extras = Array.from(extrasElements, element => {
                return {
                    name: element.dataset.name,
                    hasCost: element.dataset.hasCost,
                    cost: element.dataset.cost
                };
            });
        }

        // Determine item price, according to size and extras
        if (!isOneSize) {
            price = JSON.parse(price);
            price = price[size];
        }
        if (extras) {
            price = Number.parseFloat(price);
            extras.forEach(extra => {
                if (extra.hasCost == "true")
                    price += Number.parseFloat(extra.cost);
            });
            price = price.toFixed(2);
        }

        // Add item to the cart
        if (!localStorage.getItem('cart')) {
            const cart = JSON.stringify([{
                id: id,
                name: name,
                size: size,
                extras: extras,
                price: price
            }]);
            localStorage.setItem('cart', cart);
        }
        else {
            const cart = JSON.parse(localStorage.getItem('cart'));
            cart.push({
                id: id,
                name: name,
                size: size,
                extras: extras,
                price: price
            });
            localStorage.setItem('cart', JSON.stringify(cart));

            // console.log(' ');
            // cart.forEach(item => {
            //     console.log(item);
            // })
            // console.log(' ');
        }

        // Close the modal window
        $('#optionsModal').modal('toggle');
    };


}
