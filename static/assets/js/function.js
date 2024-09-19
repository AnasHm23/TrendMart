console.log("working fine");

const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June",
    "July", "Aug", "Sept", "Oct", "Nov", "Dec"
];

$("#commentForm").submit(function (e) {
    e.preventDefault();

    let dt = new Date();
    let time = dt.getDay() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear()

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function (res) {
            console.log("Comment Saved to DB...");

            if (res.bool == true) {
                $("#review-res").html("Review added successfully.")
                $(".hide-comment-form").hide()
                $(".add-review").hide()

                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                _html += '<div class="user justify-content-between d-flex">'
                _html += '<div class="thumb text-center">'
                _html += '<img src="https://thumbs.dreamstime.com/b/default-avatar-profile-vector-user-profile-default-avatar-profile-vector-user-profile-profile-179376714.jpg" alt="" />'
                _html += '<a href="#" class="font-heading text-brand">' + res.context.user + '</a>'
                _html += '</div>'

                _html += '<div class="desc">'
                _html += '<div class="d-flex justify-content-between mb-10">'
                _html += '<div class="d-flex align-items-center">'
                _html += '<span class="font-xs text-muted">' + time + ' </span>'
                _html += '</div>'

                for (var i = 1; i <= res.context.rating; i++) {
                    _html += '<i class="fas fa-star text-warning"></i>';
                }


                _html += '</div>'
                _html += '<p class="mb-10">' + res.context.review + '</p>'

                _html += '</div>'
                _html += '</div>'
                _html += ' </div>'

                $(".comment-list").prepend(_html)
            }


        }
    })
})

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// add to cart functionality
$(document).on("click", "#add-to-cart-btn", function() {
    let this_val = $(this);
    let index = this_val.attr("data-index");

    let quantity = $(".product-quantity-" + index).val();
    let product_title = $(".product-title-" + index).val();
    let product_image = $(".product-image-" + index).val();
    
    let product_pid = $(".product-pid-" + index).val();
    let product_id = $(".product-id-"+ index).val();
    let product_price = $(".product-price-" + index).text();

    

    console.log("quantity:", quantity)
    console.log("product_title:", product_title)
    console.log("product_id:", product_id)
    console.log("product_price:", product_price)
    console.log("product_pid:", product_pid)
    console.log("current element:", this_val)
    console.log("index:", index)
    console.log("product_image:", product_image)


    $.ajax({
        url: '/add-to-cart',
        data: {
            'qty': quantity,
            'title': product_title,
            'id': product_id,
            'price': product_price,
            'pid': product_pid,
            'image': product_image,
            'csrfmiddlewaretoken': getCSRFToken(),
        },
        dataType: 'json',
        beforeSend: function() {
            console.log("Adding product to Cart...");
        },
        success: function(response) {
            this_val.html("<i class='fi-rs-shopping-cart'></i>✓");
            console.log("Added to Cart...");
            $(".cart-items-count").text(response.totalcartitems);
        },
    })
})

// Delete product from cart
$(document).on("click", ".delete-product", function() {
    let product_id = $(this).attr("data-product");
    let this_val = $(this);

    console.log(product_id);

    $.ajax({
        url: '/delete-from-cart/',
        method: 'POST',
        data: {
            'id': product_id,
            'csrfmiddlewaretoken': getCSRFToken(),
        },
        dataType: 'json',
        beforeSend: function() {
            this_val.hide();
        },
        success: function(response) {
            if (response.totalcartitems === 0) {
                location.reload();
            } else {
                this_val.closest('tr').remove();
                $(".cart-items-count").text(response.totalcartitems);
                $(".cart-total-amount").text(response.cart_total_amount + '$');
                location.reload();
            }
        },
    });
});

// Update product from cart
$(document).on("click", ".refresh-product", function() {
    let this_val = $(this);
    let id = this_val.attr("data-product");
    let qty = this_val.closest('tr').find('.qty-product').val(); 

    console.log("Product id: " + id);
    console.log("Product qty: " + qty);

    $.ajax({
        url: '/update-cart/',
        method: 'POST',
        data: {
            'id': id,
            'qty': qty,
            'csrfmiddlewaretoken': getCSRFToken(),
        },
        dataType: 'json',
        beforeSend: function() {
            this_val.hide();
        },
        success: function(response) {
            if (response.totalcartitems === 0) {
                location.reload();
            } else {
                this_val.closest('tr').find('.qty-product').val(response.qty);
                $(".cart-items-count").text(response.totalcartitems);
                $(".cart-total-amount").text(response.cart_total_amount + '$');
                location.reload();
            }
        },
        error: function(xhr, status, error) {
            console.log("Error updating product: " + error);
            this_val.show();
        }
    });
});

// clear the cart
$(document).on("click", ".clear-all", function() {
    console.log("the cart is being cleared")
    $.ajax({
        url: '/clear-cart/',
        method: 'POST',
        data: {
            'csrfmiddlewaretoken': getCSRFToken(),
        },
        dataType: 'json',
        success: function() {
            location.reload()
        }
    });
})

// add to wishlist
$(document).on("click", "#add-to-wishlist", function() {
    let this_val = $(this);
    let index = this_val.attr("data-index");

    let product_title = $(".product-title-" + index).val();
    let product_image = $(".product-image-" + index).val();
    
    let product_pid = $(".product-pid-" + index).val();
    let product_id = $(".product-id-"+ index).val();
    let product_price = $(".product-price-" + index).text();

    console.log("product_id:", product_id)

    $.ajax({
        url: '/add-to-wishlist/',
        method: 'POST',
        data: {
            'id': product_id,
            'title': product_title,
            'price': product_price,
            'pid': product_pid,
            'image': product_image,
            'csrfmiddlewaretoken': getCSRFToken(),
        },
        beforeSend: function() {
            console.log("Adding product to Wishlist...");
        },
        success: function() {
            this_val.html("<i class='fi-rs-heart'></i>✓");
            console.log("Added to Wishlist...");
            location.reload()
        }
    })
})

// delete product from the wishlist
$(document).on("click", ".wishlist-product-delete", function() {
    let product_id = $(this).attr("data-product");

    console.log(product_id);

    $.ajax({
        url: '/delete-from-wishlist/',
        method: 'POST',
        data: {
            'id': product_id,
            'csrfmiddlewaretoken': getCSRFToken(),
        },
        dataType: 'json',
        beforeSend: function() {
            console.log("the product is being deleted from the wishlist")
        },
        success: function(response) {
            location.reload();
        },
    });
});
