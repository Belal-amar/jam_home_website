$(document).ready(function () {

    $("#product-details-modal").hide();


    $(".details-btn").click(function () {
        var productId = $(this).data("product-id"); 
        openProductModal(productId);
    });


    $(".close").click(function () {
        $("#product-details-modal").fadeOut();
    });


    $(window).click(function (event) {
        if ($(event.target).is("#product-details-modal")) {
            $("#product-details-modal").fadeOut();
        }
    });
});

function openProductModal(productId) {
    $.ajax({
        url: "/product/" + productId,
        type: "GET",
        dataType: "json",
        success: function (data) {
            if (data.error) {
                alert(data.error);
            } else {
                $("#product-name").text(data.name);
                $("#product-description").text(data.description);
                $("#product-price").text("$" + data.price);
                if (data.image_url) {
                    $("#product-image").attr("src", data.image_url);
                } else {
                    $("#product-image").attr("src", "/static/default-image.png"); 
                }
                $("#product-details-modal").fadeIn();
            }
        },
        error: function () {
            alert("Error loading product details.");
        }
    });
}


$(document).ready(function () {
    $(".details-btn").click(function () {
        let productId = $(this).data("product-id");

        $.ajax({
            url: `/product/${productId}/details/`,
            method: "GET",
            success: function (data) {
                $("#product-name").text(data.name);
                $("#product-image").attr("src", data.image);
                $("#product-description").text(data.description);
                $("#product-price").text(data.price);
                $("#add-to-cart-btn").data("product-id", data.id);
                $("#product-details-modal").show();
            },
        });
    });

    $("#add-to-cart-btn").click(function () {
        let productId = $(this).data("product-id");

        $.ajax({
            url: "/add-to-cart/",
            method: "POST",
            data: {
                product_id: productId,
                quantity: 1,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            },
            success: function (response) {
                alert(response.message);
            },
        });
    });

    $(".close").click(function () {
        $("#product-details-modal").hide();
    });
});
