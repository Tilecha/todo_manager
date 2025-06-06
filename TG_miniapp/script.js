const content = document.getElementById('content');

const data = {
  profile: '<h2>Мой кабинет</h2><p>Профиль пользователя, настройки и прочее.</p>',
  tasks: '<h2>Мои задачи</h2><p>Список ваших текущих задач.</p>',
};

const buttons = document.querySelectorAll('button');

buttons.forEach(button => {
  button.addEventListener('click', () => {
    buttons.forEach(btn => btn.classList.remove('active'));
    
    button.classList.add('active');
    
    const id = button.id;
    content.innerHTML = data[id] || 'Контент не найден.';
  });
});
