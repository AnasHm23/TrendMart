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


// add to cart functionality
$(document).on("click", "#add-to-cart-btn", function() {
    let this_val = $(this);
    let index = this_val.attr("data-index");

    let quantity = $(".product-quantity-" + index).val();
    let product_title = $(".product-title-" + index).val();
    let product_image = $(".product-image-" + index).val();
    
    let product_pid = $(".product-pid-" + index).val();
    let product_id = $(".product-id-"+ index).val();
    let product_price = $("#product-price-" + index).text();
    

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
