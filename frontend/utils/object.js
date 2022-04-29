export function updateByPath(target, path, value) {
  if (Array.isArray(path)) {
    if (path.length === 0) {
      return value
    } else {
      const key = path[0]
      if (isNaN(key)) {
        target = target || {}
        target[key] = updateByPath(target[key], path.slice(1), value)
      } else {
        target = target || []
        target[parseInt(key)] = updateByPath(target[key], path.slice(1), value)
      }
      return target
    }
  } else {
    return updateByPath(target, path.split('.'), value)
  }
}
