export function changeSelectors(dropdown, selector) {
    const options = {
        1: ['Кодировка - 8 бит', 'Кодировка - 16 бит'],
        2: ['Шифр из символов', 'Шифр из цифр'],
        3: ['Наибольшее значение', 'Наименьшее значение', 'Неизвестное значение'],
        4: [],
        5: [],
        6: [],
        7: [],
        8: ['Запрос - 1 слово', 'Запрос - 2 слова'],
        9: ['Поиск путей', 'Поиск путей с условием'],
        10: ['Арифметические вычисления', 'Поиск числа', 'Перевод систем счисления'],
        11: [],
        12: []
    }
    const selectionText = dropdown[dropdown.selectedIndex].text
    const selection = selectionText.split(' ')[1]
    selector.selectedIndex = 0
    while (selector.options.length > 0) {
        selector.remove(0)
    }
    selector.options[selector.options.length] = new Option('Все типы')

    for (let name of options[selection]) {
        const option = new Option(name, undefined)
        selector.options.add(option)
    }
}









