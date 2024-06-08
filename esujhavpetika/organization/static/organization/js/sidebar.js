 
function checkScreenWidth() {
  if (window.innerWidth < 768) {
      document.querySelector('.sidebar').style.display = 'none';
  } else {
      document.querySelector('.sidebar').style.display = 'block';
  }
}
window.addEventListener('resize', checkScreenWidth);
window.addEventListener('load', checkScreenWidth);

document.getElementById('sidebarToggle').addEventListener('click', function() {
  var sidebar = document.querySelector('.sidebar');
  if (sidebar.style.display === 'block' || sidebar.style.display === '') {
      sidebar.style.display = 'none';
  } else {
      sidebar.style.display = 'block';
  }
});

document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', function() {
      document.querySelectorAll('.nav-link').forEach(item => {
          item.classList.remove('active');
      });
      this.classList.add('active');
  });
});
 
document.addEventListener('DOMContentLoaded', function() {
  let currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
      if (link.getAttribute('href') === currentPath && !link.href.includes('signout')) {
          link.classList.add('active');
      }
  });
});