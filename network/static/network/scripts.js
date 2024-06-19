document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.heartcontainer').forEach(function(like)
    {
      like.addEventListener('click', function(){
        let user = like.getAttribute('data-user');
        let post= like.getAttribute('data-post')
        fetch('/update_likes/', {
          method: 'POST', 
          body: JSON.stringify({
              'likes': user, // replace with your actual data
              'post': post
          })
      })
      .then(response => response.json())
      .then(data => {
      console.log(data);
      document.querySelector(`#likes-count-${post}`).innerHTML = data.new_likes_count;
      });
      });
    }); 
  });
  

//like and unlike post

//edit post


  