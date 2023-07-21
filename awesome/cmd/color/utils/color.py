def relative_luminance(r_8bit: int, g_8bit: int, b_8bit: int) -> float:
    # https://www.w3.org/TR/WCAG20/#relativeluminancedef
    r_srgb, g_srgb, b_srgb = r_8bit / 255, g_8bit / 255, b_8bit / 255
    r = r_srgb / 12.92 if r_srgb <= 0.03928 else ((r_srgb + 0.055) / 1.055) ** 2.4
    g = g_srgb / 12.92 if g_srgb <= 0.03928 else ((g_srgb + 0.055) / 1.055) ** 2.4
    b = b_srgb / 12.92 if b_srgb <= 0.03928 else ((b_srgb + 0.055) / 1.055) ** 2.4
    l = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return l


def contrast_ratio(l1: float, l2: float) -> float:
    # https://www.w3.org/TR/WCAG20/#contrast-ratiodef
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)
