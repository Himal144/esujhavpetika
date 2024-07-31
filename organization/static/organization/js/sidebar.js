function checkScreenWidth() {
  if (window.innerWidth < 768) {
      document.querySelector('.sidebar').classList.add('collapsed');
      document.querySelector('#sidebarToggle').style.display = 'block';
  } else {
      document.querySelector('.sidebar').classList.remove('collapsed');
      document.querySelector('#sidebarToggle').style.display = 'none';
  }
}

window.addEventListener('resize', checkScreenWidth);
window.addEventListener('load', checkScreenWidth);

document.getElementById('sidebarToggle').addEventListener('click', function() {
  var sidebar = document.querySelector('.sidebar');
  if (sidebar.classList.contains('collapsed')) {
      sidebar.classList.remove('collapsed');
  } else {
      sidebar.classList.add('collapsed');
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