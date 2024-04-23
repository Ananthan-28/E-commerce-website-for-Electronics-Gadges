    $(document).ready(function() {

        $('#carouselExampleIndicators').carousel();


        $('.thumbnail').on('click', function() {
            var slideIndex = $(this).data('slide-to');
            $('#carouselExampleIndicators').carousel(slideIndex);
        });
    });

  $(document).ready(function() {

      $('.rating i').on('click', function() {
        var rating = $(this).data('rating');
        $('#rating').val(rating);
        $(this).addClass('bi-star-fill').removeClass('bi-star').prevAll().addClass('bi-star-fill').removeClass('bi-star').end().nextAll().removeClass('bi-star-fill').addClass('bi-star');
      });

      $('#reviewForm').on('submit', function(e) {
        e.preventDefault();
        var review = $('#review').val();
        var rating = $('#rating').val();

        console.log("Review:", review);
        console.log("Rating:", rating);

        $('#ReviewModal').modal('hide');
      });
    });

    function checkInput() {
        var searchData = document.getElementById('searchData').value;
        if (searchData.trim() !== '') {
            document.getElementById('submitButton').disabled = false;
        } else {
            document.getElementById('submitButton').disabled = true;
        }
    }
