jQuery(function ($) {
    $(document).on("click", ".sidebar-dropdown > a", function () {
        $(".sidebar-submenu").slideUp(200);
        if ($(this).parent().hasClass("active")) {
            $(".sidebar-dropdown").removeClass("active");
            $(this).parent().removeClass("active");
        } else {
            $(".sidebar-dropdown").removeClass("active");
            $(this).next(".sidebar-submenu").slideDown(200);
            $(this).parent().addClass("active");
        }
    });

    $(document).on("click", "#close-sidebar", function () {
        $(".page-wrapper").removeClass("toggled");
    });

    $(document).on("click", "#show-sidebar", function () {
        $(".page-wrapper").addClass("toggled");
    });
});