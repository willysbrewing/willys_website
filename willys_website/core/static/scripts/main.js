'use strict';
(function() {

    $(function(){

        /************ SW *************/

        if ('serviceWorker' in navigator) {
          window.addEventListener('load', function() {
            navigator.serviceWorker.register('/static/scripts/sw.js').then(function(registration) {
              // Registration was successful
              console.log('ServiceWorker registration successful with scope: ', registration.scope);
            }).catch(function(err) {
              // registration failed :(
              console.log('ServiceWorker registration failed: ', err);
            });
          });
        }

        /************ COOKIES *************/

        function getCookie(cname) {
            var name = cname + '=';
            var ca = document.cookie.split(';');
            for(var i=0; i<ca.length; i++) {
                var c = ca[i];
                while (c.charAt(0)===' ') {c = c.substring(1);}
                if (c.indexOf(name) === 0) {return c.substring(name.length,c.length);}
            }
            return '';
        }

        function setCookie(cname, cvalue, exdays) {
            var d = new Date();
            d.setTime(d.getTime() + (exdays*24*60*60*1000));
            var expires = 'expires='+d.toUTCString();
            document.cookie = cname + '=' + cvalue + '; ' + expires+"; path=/";
        }

        (function(){
          function showPolicy(){
            $('.cookies').show();
          }
          function showAgeModal(){
            var ageModal = $('#ageModal');
            ageModal.modal({
              backdrop: 'static',
              keyboard: false
            });
            ageModal.find('#nop').on('click', function(){
              ageModal.find('.modal-body').html('<p style="font-size:15px;">Demasiado peque para entrar... vuelve en unos años, te guardaremos una birra 😎</p>');
            });
            ageModal.find('#yep').on('click', function(){
              setCookie('wb_a', 1, 365);
              ageModal.modal('hide');
            });
            ageModal.modal('show');
          }
          if(parseInt(getCookie('wb_p')) !== 1){
            showPolicy();
            setCookie('wb_p', 1, 365);
            $('.cookies .close').click(function() {
              $('.cookies').fadeOut();
            })
          }
          if(parseInt(getCookie('wb_a')) !== 1){
            showAgeModal();
          }
        })();

        /************ NAVBAR *************/

        var navbar_menu_visible = 0;
        var navbar_initialized = false;

        function initRightMenu(){

            if(!navbar_initialized){
                var $navbar = $('nav').find('.navbar-collapse').first().clone(true);

                var ul_content = '';

                $navbar.children('ul').each(function(){
                    var content_buff = $(this).html();
                    ul_content = ul_content + content_buff;
                });

                ul_content = '<ul class="nav navbar-nav">' + ul_content + '</ul>';
                $navbar.html(ul_content);

                $('body').append($navbar);

                var $toggle = $('.navbar-toggle');

                $navbar.find('a').removeClass('btn btn-round btn-default');
                $navbar.find('button').removeClass('btn-round btn-fill btn-info btn-primary btn-success btn-danger btn-warning btn-neutral');
                $navbar.find('button').addClass('btn-simple btn-block');

                $toggle.click(toggleSidebarMenu);

                navbar_initialized = true;
            }
        }

        function toggleSidebarMenu(){
            if(navbar_menu_visible == 1) {
                $('html').removeClass('nav-open');
                navbar_menu_visible = 0;
                $('.body-click').remove();
                 setTimeout(function(){
                     var $toggle = $('.navbar-toggle');
                    $toggle.removeClass('toggled');
                 }, 400);

            } else {
                setTimeout(function(){
                    var $toggle = $('.navbar-toggle');
                    $toggle.addClass('toggled');
                }, 430);

                var div = '<div class="body-click"></div>';
                $(div).appendTo("body").click(function() {
                    $('html').removeClass('nav-open');
                    navbar_menu_visible = 0;
                    $('.body-click').remove();
                     setTimeout(function(){
                         var $toggle = $('.navbar-toggle');
                        $toggle.removeClass('toggled');
                     }, 400);
                });

                $('html').addClass('nav-open');
                navbar_menu_visible = 1;
            }
        }

        // init smooth links
        $('a.smooth').click(function(e) {
            e.preventDefault();
            var $link = $(this);
            var anchor = $link.attr('href');
            $('html, body').stop().animate({
                scrollTop : $(anchor).offset().top
            }, 500);
            return false;
        });

        //Index video autoplay at load
        if($('.supervideo').get(0) !== undefined){
          $('.supervideo').get(0).play();
        }

        var window_width = $(window).width();
        var burger_menu = $('nav[role="navigation"]').hasClass('navbar-burger') ? true : false;
        // Init navigation toggle for small screens
        if(window_width < 768 || burger_menu){
            initRightMenu();
        }

        // Do not delay load of page with async functionality: Wait for window load
        window.addEventListener('load', function(){


        }); // End of window load

        $(window).resize(function(){

            var burger_menu = $('nav[role="navigation"]').hasClass('navbar-burger') ? true : false;
            if($(window).width() < 768){
                initRightMenu();
            } else if(!burger_menu && navbar_menu_visible){
                toggleSidebarMenu();
            }

        }); // End of window resize

    }); // End of jQuery context

})(); // End of use strict
