export function formatNumber(num: number): string {
  try {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  } catch (error) {
    console.error(error);
    return "NaN";
  }
}
