"use client";
import {
  require_jsx_runtime,
  require_prop_types,
  require_react_is2 as require_react_is
} from "./chunk-C2L7XJJ2.js";
import {
  require_react
} from "./chunk-OELA7GPI.js";
import {
  __toESM
} from "./chunk-G3PMV62Z.js";

// node_modules/.pnpm/@mui+base@5.0.0-beta.58_@types+react@18.3.8_react-dom@18.3.1_react@18.3.1__react@18.3.1/node_modules/@mui/base/TextareaAutosize/TextareaAutosize.js
var React12 = __toESM(require_react());
var import_prop_types4 = __toESM(require_prop_types());

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/chainPropTypes/chainPropTypes.js
function chainPropTypes(propType1, propType2) {
  if (false) {
    return () => null;
  }
  return function validate(...args) {
    return propType1(...args) || propType2(...args);
  };
}

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/elementAcceptingRef/elementAcceptingRef.js
var import_prop_types = __toESM(require_prop_types());
function isClassComponent(elementType) {
  const {
    prototype = {}
  } = elementType;
  return Boolean(prototype.isReactComponent);
}
function acceptingRef(props, propName, componentName, location, propFullName) {
  const element = props[propName];
  const safePropName = propFullName || propName;
  if (element == null || // When server-side rendering React doesn't warn either.
  // This is not an accurate check for SSR.
  // This is only in place for Emotion compat.
  // TODO: Revisit once https://github.com/facebook/react/issues/20047 is resolved.
  typeof window === "undefined") {
    return null;
  }
  let warningHint;
  const elementType = element.type;
  if (typeof elementType === "function" && !isClassComponent(elementType)) {
    warningHint = "Did you accidentally use a plain function component for an element instead?";
  }
  if (warningHint !== void 0) {
    return new Error(`Invalid ${location} \`${safePropName}\` supplied to \`${componentName}\`. Expected an element that can hold a ref. ${warningHint} For more information see https://mui.com/r/caveat-with-refs-guide`);
  }
  return null;
}
var elementAcceptingRef = chainPropTypes(import_prop_types.default.element, acceptingRef);
elementAcceptingRef.isRequired = chainPropTypes(import_prop_types.default.element.isRequired, acceptingRef);

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/elementTypeAcceptingRef/elementTypeAcceptingRef.js
var import_prop_types2 = __toESM(require_prop_types());
function isClassComponent2(elementType) {
  const {
    prototype = {}
  } = elementType;
  return Boolean(prototype.isReactComponent);
}
function elementTypeAcceptingRef(props, propName, componentName, location, propFullName) {
  const propValue = props[propName];
  const safePropName = propFullName || propName;
  if (propValue == null || // When server-side rendering React doesn't warn either.
  // This is not an accurate check for SSR.
  // This is only in place for emotion compat.
  // TODO: Revisit once https://github.com/facebook/react/issues/20047 is resolved.
  typeof window === "undefined") {
    return null;
  }
  let warningHint;
  if (typeof propValue === "function" && !isClassComponent2(propValue)) {
    warningHint = "Did you accidentally provide a plain function component instead?";
  }
  if (warningHint !== void 0) {
    return new Error(`Invalid ${location} \`${safePropName}\` supplied to \`${componentName}\`. Expected an element type that can hold a ref. ${warningHint} For more information see https://mui.com/r/caveat-with-refs-guide`);
  }
  return null;
}
var elementTypeAcceptingRef_default = chainPropTypes(import_prop_types2.default.elementType, elementTypeAcceptingRef);

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/getDisplayName/getDisplayName.js
var import_react_is = __toESM(require_react_is());

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/ponyfillGlobal/ponyfillGlobal.js
var ponyfillGlobal_default = typeof window != "undefined" && window.Math == Math ? window : typeof self != "undefined" && self.Math == Math ? self : Function("return this")();

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/refType/refType.js
var import_prop_types3 = __toESM(require_prop_types());
var refType = import_prop_types3.default.oneOfType([import_prop_types3.default.func, import_prop_types3.default.object]);

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/debounce/debounce.js
function debounce(func, wait = 166) {
  let timeout;
  function debounced(...args) {
    const later = () => {
      func.apply(this, args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  }
  debounced.clear = () => {
    clearTimeout(timeout);
  };
  return debounced;
}

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/isMuiElement/isMuiElement.js
var React = __toESM(require_react());

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/ownerDocument/ownerDocument.js
function ownerDocument(node) {
  return node && node.ownerDocument || document;
}

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/ownerWindow/ownerWindow.js
function ownerWindow(node) {
  const doc = ownerDocument(node);
  return doc.defaultView || window;
}

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/setRef/setRef.js
function setRef(ref, value) {
  if (typeof ref === "function") {
    ref(value);
  } else if (ref) {
    ref.current = value;
  }
}

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/useEnhancedEffect/useEnhancedEffect.js
var React2 = __toESM(require_react());
var useEnhancedEffect = typeof window !== "undefined" ? React2.useLayoutEffect : React2.useEffect;
var useEnhancedEffect_default = useEnhancedEffect;

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/useId/useId.js
var React3 = __toESM(require_react());
var maybeReactUseId = React3["useId".toString()];

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/useControlled/useControlled.js
var React4 = __toESM(require_react());

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/useEventCallback/useEventCallback.js
var React5 = __toESM(require_react());

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/useForkRef/useForkRef.js
var React6 = __toESM(require_react());
function useForkRef(...refs) {
  return React6.useMemo(() => {
    if (refs.every((ref) => ref == null)) {
      return null;
    }
    return (instance) => {
      refs.forEach((ref) => {
        setRef(ref, instance);
      });
    };
  }, refs);
}

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/useLazyRef/useLazyRef.js
var React7 = __toESM(require_react());

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/useOnMount/useOnMount.js
var React8 = __toESM(require_react());

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/usePreviousProps/usePreviousProps.js
var React9 = __toESM(require_react());

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/getValidReactChildren/getValidReactChildren.js
var React10 = __toESM(require_react());

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/integerPropType/integerPropType.js
function getTypeByValue(value) {
  const valueType = typeof value;
  switch (valueType) {
    case "number":
      if (Number.isNaN(value)) {
        return "NaN";
      }
      if (!Number.isFinite(value)) {
        return "Infinity";
      }
      if (value !== Math.floor(value)) {
        return "float";
      }
      return "number";
    case "object":
      if (value === null) {
        return "null";
      }
      return value.constructor.name;
    default:
      return valueType;
  }
}
function requiredInteger(props, propName, componentName, location) {
  const propValue = props[propName];
  if (propValue == null || !Number.isInteger(propValue)) {
    const propType = getTypeByValue(propValue);
    return new RangeError(`Invalid ${location} \`${propName}\` of type \`${propType}\` supplied to \`${componentName}\`, expected \`integer\`.`);
  }
  return null;
}
function validator(props, propName, ...other) {
  const propValue = props[propName];
  if (propValue === void 0) {
    return null;
  }
  return requiredInteger(props, propName, ...other);
}
function validatorNoop() {
  return null;
}
validator.isRequired = requiredInteger;
validatorNoop.isRequired = validatorNoop;

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/ClassNameGenerator/ClassNameGenerator.js
var defaultGenerator = (componentName) => componentName;
var createClassNameGenerator = () => {
  let generate = defaultGenerator;
  return {
    configure(generator) {
      generate = generator;
    },
    generate(componentName) {
      return generate(componentName);
    },
    reset() {
      generate = defaultGenerator;
    }
  };
};
var ClassNameGenerator = createClassNameGenerator();

// node_modules/.pnpm/@mui+utils@6.0.0-rc.0_@types+react@18.3.8_react@18.3.1/node_modules/@mui/utils/esm/getReactNodeRef/getReactNodeRef.js
var React11 = __toESM(require_react());

// node_modules/.pnpm/@mui+base@5.0.0-beta.58_@types+react@18.3.8_react-dom@18.3.1_react@18.3.1__react@18.3.1/node_modules/@mui/base/TextareaAutosize/TextareaAutosize.js
var import_jsx_runtime = __toESM(require_jsx_runtime());
function getStyleValue(value) {
  return parseInt(value, 10) || 0;
}
var styles = {
  shadow: {
    // Visibility needed to hide the extra text area on iPads
    visibility: "hidden",
    // Remove from the content flow
    position: "absolute",
    // Ignore the scrollbar width
    overflow: "hidden",
    height: 0,
    top: 0,
    left: 0,
    // Create a new layer, increase the isolation of the computed values
    transform: "translateZ(0)"
  }
};
function isEmpty(obj) {
  return obj === void 0 || obj === null || Object.keys(obj).length === 0 || obj.outerHeightStyle === 0 && !obj.overflowing;
}
var TextareaAutosize = React12.forwardRef(function TextareaAutosize2(props, forwardedRef) {
  const {
    onChange,
    maxRows,
    minRows = 1,
    style,
    value,
    ...other
  } = props;
  const {
    current: isControlled
  } = React12.useRef(value != null);
  const inputRef = React12.useRef(null);
  const handleRef = useForkRef(forwardedRef, inputRef);
  const heightRef = React12.useRef(null);
  const shadowRef = React12.useRef(null);
  const calculateTextareaStyles = React12.useCallback(() => {
    const input = inputRef.current;
    const containerWindow = ownerWindow(input);
    const computedStyle = containerWindow.getComputedStyle(input);
    if (computedStyle.width === "0px") {
      return {
        outerHeightStyle: 0,
        overflowing: false
      };
    }
    const inputShallow = shadowRef.current;
    inputShallow.style.width = computedStyle.width;
    inputShallow.value = input.value || props.placeholder || "x";
    if (inputShallow.value.slice(-1) === "\n") {
      inputShallow.value += " ";
    }
    const boxSizing = computedStyle.boxSizing;
    const padding = getStyleValue(computedStyle.paddingBottom) + getStyleValue(computedStyle.paddingTop);
    const border = getStyleValue(computedStyle.borderBottomWidth) + getStyleValue(computedStyle.borderTopWidth);
    const innerHeight = inputShallow.scrollHeight;
    inputShallow.value = "x";
    const singleRowHeight = inputShallow.scrollHeight;
    let outerHeight = innerHeight;
    if (minRows) {
      outerHeight = Math.max(Number(minRows) * singleRowHeight, outerHeight);
    }
    if (maxRows) {
      outerHeight = Math.min(Number(maxRows) * singleRowHeight, outerHeight);
    }
    outerHeight = Math.max(outerHeight, singleRowHeight);
    const outerHeightStyle = outerHeight + (boxSizing === "border-box" ? padding + border : 0);
    const overflowing = Math.abs(outerHeight - innerHeight) <= 1;
    return {
      outerHeightStyle,
      overflowing
    };
  }, [maxRows, minRows, props.placeholder]);
  const syncHeight = React12.useCallback(() => {
    const textareaStyles = calculateTextareaStyles();
    if (isEmpty(textareaStyles)) {
      return;
    }
    const outerHeightStyle = textareaStyles.outerHeightStyle;
    const input = inputRef.current;
    if (heightRef.current !== outerHeightStyle) {
      heightRef.current = outerHeightStyle;
      input.style.height = `${outerHeightStyle}px`;
    }
    input.style.overflow = textareaStyles.overflowing ? "hidden" : "";
  }, [calculateTextareaStyles]);
  useEnhancedEffect_default(() => {
    const handleResize = () => {
      syncHeight();
    };
    let rAF;
    const rAFHandleResize = () => {
      cancelAnimationFrame(rAF);
      rAF = requestAnimationFrame(() => {
        handleResize();
      });
    };
    const debounceHandleResize = debounce(handleResize);
    const input = inputRef.current;
    const containerWindow = ownerWindow(input);
    containerWindow.addEventListener("resize", debounceHandleResize);
    let resizeObserver;
    if (typeof ResizeObserver !== "undefined") {
      resizeObserver = new ResizeObserver(false ? rAFHandleResize : handleResize);
      resizeObserver.observe(input);
    }
    return () => {
      debounceHandleResize.clear();
      cancelAnimationFrame(rAF);
      containerWindow.removeEventListener("resize", debounceHandleResize);
      if (resizeObserver) {
        resizeObserver.disconnect();
      }
    };
  }, [calculateTextareaStyles, syncHeight]);
  useEnhancedEffect_default(() => {
    syncHeight();
  });
  const handleChange = (event) => {
    if (!isControlled) {
      syncHeight();
    }
    if (onChange) {
      onChange(event);
    }
  };
  return (0, import_jsx_runtime.jsxs)(React12.Fragment, {
    children: [(0, import_jsx_runtime.jsx)("textarea", {
      value,
      onChange: handleChange,
      ref: handleRef,
      rows: minRows,
      style,
      ...other
    }), (0, import_jsx_runtime.jsx)("textarea", {
      "aria-hidden": true,
      className: props.className,
      readOnly: true,
      ref: shadowRef,
      tabIndex: -1,
      style: {
        ...styles.shadow,
        ...style,
        paddingTop: 0,
        paddingBottom: 0
      }
    })]
  });
});
true ? TextareaAutosize.propTypes = {
  // ┌────────────────────────────── Warning ──────────────────────────────┐
  // │ These PropTypes are generated from the TypeScript type definitions. │
  // │ To update them, edit the TypeScript types and run `pnpm proptypes`. │
  // └─────────────────────────────────────────────────────────────────────┘
  /**
   * @ignore
   */
  className: import_prop_types4.default.string,
  /**
   * Maximum number of rows to display.
   */
  maxRows: import_prop_types4.default.oneOfType([import_prop_types4.default.number, import_prop_types4.default.string]),
  /**
   * Minimum number of rows to display.
   * @default 1
   */
  minRows: import_prop_types4.default.oneOfType([import_prop_types4.default.number, import_prop_types4.default.string]),
  /**
   * @ignore
   */
  onChange: import_prop_types4.default.func,
  /**
   * @ignore
   */
  placeholder: import_prop_types4.default.string,
  /**
   * @ignore
   */
  style: import_prop_types4.default.object,
  /**
   * @ignore
   */
  value: import_prop_types4.default.oneOfType([import_prop_types4.default.arrayOf(import_prop_types4.default.string), import_prop_types4.default.number, import_prop_types4.default.string])
} : void 0;
export {
  TextareaAutosize
};
//# sourceMappingURL=@mui_base_TextareaAutosize.js.map
