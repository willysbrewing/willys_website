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

        // Form
        var welcomeForm = document.getElementById('register-form');
        if (welcomeForm) {
          if (welcomeForm.attachEvent) {
              welcomeForm.attachEvent('submit', processWelcomeForm);
          } else {
              welcomeForm.addEventListener('submit', processWelcomeForm);
          }
        }

        function processWelcomeForm(e) {
          if (e.preventDefault) e.preventDefault();

          try{
            var form = document.getElementById('register-form');
            var email = form.querySelector('#inputEmail').value;
            var policy = form.querySelector('#policy').checked;

            if(email && policy){
              form.querySelector('#inputEmail').style.borderColor = 'inherit';
              form.querySelector('#policy').style.borderColor = 'inherit';
              var data = {email:email};
              var leadFormButton = document.getElementById('lead-form-button');
              leadFormButton.style.display = 'none';
              var processing = document.getElementById('processing-form');
              processing.style.display = 'block';
              try{
                // SendMail
                sendEmail('c348a464-4240-4cf4-9c88-7b2c892070d7', data);

                // Track Event
                dataLayer.push({'event': 'lead_real'});

                processing.style.display = 'none';
                var success = document.getElementById('success-form');
                success.style.display = 'block';
              }
              catch(e){}
            }
            else {
              if (!email || email === "") {
                form.querySelector('#inputEmail').style.borderColor = 'red';
              }
              if (!policy) {
                form.querySelector('#policy').style.borderColor = 'red';
              }
            }
          } catch(e){}
          return false;
        }

        // ContactForm
        var contactForm = document.getElementById('contact-form');
        if (contactForm) {
          if (contactForm.attachEvent) {
              contactForm.attachEvent('submit', processContactForm);
          } else {
              contactForm.addEventListener('submit', processContactForm);
          }
        }

        function processContactForm(e) {
          if (e.preventDefault) e.preventDefault();

          try{
            var form = document.getElementById('contact-form');
            var email = form.querySelector('#inputEmail').value;
            var policy = form.querySelector('#policy').checked;
            var content = form.querySelector('#content').value;

            if(email && policy && content){
              form.querySelector('#inputEmail').style.borderColor = 'inherit';
              form.querySelector('#content').style.borderColor = 'inherit';
              form.querySelector('#policy').style.borderColor = 'inherit';
              var data = {email:'contacto@willysbrewing.com', content:content, from:email};
              var leadFormButton = document.getElementById('lead-form-button');
              leadFormButton.style.display = 'none';
              var processing = document.getElementById('processing-form');
              processing.style.display = 'block';
              try{
                // SendMail
                sendEmail('b9e4a79f-5bd0-4ba9-b0b1-4a6a64df9156', data);

                // Track Event
                dataLayer.push({'event': 'contact_form'});

                processing.style.display = 'none';
                var success = document.getElementById('success-form');
                success.style.display = 'block';
              }
              catch(e){}
            }
            else {
              if (!email || email === "") {
                form.querySelector('#inputEmail').style.borderColor = 'red';
              }
              if (!content || content === "") {
                form.querySelector('#content').style.borderColor = 'red';
              }
              if (!policy) {
                form.querySelector('#policy').style.borderColor = 'red';
              }
            }
          } catch(e){}
          return false;
        }

        function sendEmail(id, data){
          var url = 'https://notifications.api.willysbrewing.com/mail/send';
          var q = new XMLHttpRequest();
          q.open('POST', url, true);
          q.setRequestHeader('Content-Type', 'application/json');
          q.onreadystatechange = function(){
            if(this.readyState === 4){
              if(this.status.toString()[0] == '2'){
                // ok
              }
              else if(this.status.toString()[0] == '4' || this.status.toString()[0] == '5'){
                // error
              }
              else{
                // foo
              }
            }
          };
          var payload = {
            'recipient': data.email,
            'subject': data.subject || '',
            'content': data.content || '',
            'template':{
              'id': id,
              'data':{
                'name': data.name || 'notset',
                'from': data.from || 'notset',
                'content': data.content || 'notset'
              }
            }
          };
          q.send(JSON.stringify(payload));
        }

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
