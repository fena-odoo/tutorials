import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(refName) {
  const elRef = useRef(refName);
  onMounted(() => {
    if (elRef.el) {
      elRef.el.focus();
    }
  });
  return elRef;
}
