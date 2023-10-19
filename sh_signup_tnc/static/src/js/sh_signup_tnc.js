odoo.define("sh_signup_tnc.web_auth", function (require) {
    "use strict";

    $(document).ready(function () {
        const show_terms = document.getElementById("show_terms_website_auth")
        if (show_terms) {
            $(".oe_login_buttons").find(":submit").prop('disabled', true)
        } else {
            $(".oe_login_buttons").find(":submit").prop('disabled', false)
        }

        $("#chk_terms_auth").on("change", function () {
            if ($(this).is(":checked")) {
                $(".oe_login_buttons").find(":submit").prop('disabled', false)
            } else {
                $(".oe_login_buttons").find(":submit").prop('disabled', true)
            }
        });
    });
});
