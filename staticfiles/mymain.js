document.getElementById('id_brands').addEventListener('mouseover', function (e) {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var output = JSON.parse(this.response);
            // console.log(typeof output)
            // console.log(output[1]['fields']['subcatname'])
            var t = ''
            for (var i = 0; i < output.length; i++) {
                // console.log(output[i]['fields']['name'])
                t += `<li class="nav-item"><a class="nav-link" href="/Shopping/search?searchbar=${output[i]['fields']['name']}">${output[i]['fields']['name']}</a></li>`
            }
            document.getElementById('id_brands_data').innerHTML = t
        }
    };
    // xml.open('GET', 'http://127.0.0.1:8000/Shopping/categorydata', true);
    xml.open('GET', '/Shopping/categorydata', true);
    xml.send()
});

// document.getElementById('shopping_cart').addEventListener('onclick',function (e) {
//     console.log(document.querySelector('.mycart').id)
// })

function cart(id) {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var output = this.response
            document.getElementById('cart-bar').innerHTML = " " + output;
        }
    };
    xml.open('GET', `/Shopping/cart/add/${id}/`, true)
    xml.send()
}

function cartupdate(status, id) {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var output = JSON.parse(this.response);
            console.log(output);
            document.getElementById('sst' + id).value = output.qty
            document.getElementById('total' + id).innerHTML = output['total']
            document.getElementById('grandtotal').innerHTML = output['grandtotal']
        }
    };
    if (status == 'increment') {
        xml.open('GET', `/Shopping/cart/item_increment/${id}/`, true)
    } else if (status == 'decrement') {
        console.log(document.getElementById('sst' + id).value)
        if (parseInt(document.getElementById('sst' + id).value) <= 1) {
            console.log('do nothing')
        } else {
            xml.open('GET', `/Shopping/cart/item_decrement/${id}/`, true)
        }
    }
    xml.send()
}

function deletecard(id) {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            window.location.href = '/Shopping/cart/cart-detail/'
        }
    };
    xml.open('GET', `/Shopping/cart/item_clear/${id}/`, true);
    xml.send()
}

function billdetail(id) {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var output = JSON.parse(this.response);
            console.log(output)
            var t = ''
            for (var i = 0; i < output.length; i++) {
                console.log(output[i]);
                t += `<tr>`
                t += `<td>${output[i]['fields']['proid']}</td>`
                t += `<td>${output[i]['fields']['qty']}</td>`
                t += `<td>${output[i]['fields']['price']}</td>`
                t += `</tr>`
            }
            document.getElementById('bildet').innerHTML = t
            console.log(t)
            $('#myModal').modal('show')
        }
    };
    xml.open('GET', '/Shopping/bill/billdetail/' + id, true);
    xml.send();
}



function wistlist(id) {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var output = this.response
            document.getElementById('wishlist-bar').innerHTML = " " + output;
        }
    };
    xml.open('GET', `/Shopping/wishlist/add/${id}/`, true)
    xml.send()
}



function compareList(id) {
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var output = this.response
            document.getElementById('compareList-bar').innerHTML = " " + output;
        }
    };
    xml.open('GET', `/Shopping/compareList/add/${id}/`, true)
    xml.send()
}

