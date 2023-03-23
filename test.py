import re

htmlstr = """
<ul>
<li><strong>HiBar's Maintain Shampoo Bar:</strong> This bar is formulated to gently cleanse and hydrate color-treated hair. It's free of sulfates, parabens, and silicone, making it a great option for those with sensitive scalps.</li>
<li><strong>Ethique's Pinkalicious:</strong> This bar is perfect for those with pink or red hair. It's formulated with pink grapefruit and lime oils to help maintain the color and prevent fading.</li>
<li><strong>Lush's Copperhead:</strong> This bar is specifically formulated for those with copper-colored hair. It contains henna and coffee to help enhance and maintain the color.</li>
</ul>
 """


def format_html(html_str):
    # 定义匹配的正则表达式
    pattern = re.compile(r"^<(p|h1|h2|h3|li)>.*<\/\1>$")
    pattern_img = re.compile(r"^<img\s.*\s?\/?>$")
    html_str = html_str.replace('<div>', '')
    html_str = html_str.replace('</div>', '')
    # 剔除所有div
    # 定义一个空列表，用于存放处理后的每个元素
    wrapped_arr = []
    # 循环遍历每个元素并添加包裹符号
    for elem in html_str.split('\n'):
        if not html_str.__contains__('<p>') and not html_str.__contains__('ul>'):
            wrapped_arr.append(f"<p>{elem}</p>")
        else:
            result = pattern.match(elem) or pattern_img.match(elem) or elem.__contains__('ul>')
            wrapped_elem = elem
            if result:
                wrapped_arr.append(wrapped_elem)
        # 使用join()方法将所有元素合并成一个字符串
        embroidery_data = "\n".join(wrapped_arr)
    return embroidery_data


print(format_html(htmlstr))
