const fableUtils = require('fable-utils')
const path_ = require('path')
const babel = require('babel-core')
const fs = require('fs')

const ensureArray = (obj) => (Array.isArray(obj) ? obj : obj != null ? [obj] : [])

async function parse(path, isProjectFile = false) {
  const isProduction = process.env.NODE_ENV === 'production'
  const port =
    process.env.FABLE_SERVER_PORT != null ? parseInt(process.env.FABLE_SERVER_PORT, 10) : 61225

  let msg = {
    path,
    define: isProduction ? [] : ['DEBUG'],
  }

  const response = await fableUtils.client.send(port, JSON.stringify(msg))

  // the project file doesn't need to be transpiled, just sent to fable
  if (isProjectFile) return

  const data = JSON.parse(response)

  const { error = null, logs = {} } = data

  if (error || ensureArray(logs.error).length > 0) {
    // TODO: figure out how to deal with the error variable

    return { ...logs, success: false }
  } else {
    const babelOpts = fableUtils.resolveBabelOptions({
      plugins: [],
      sourceMaps: false,
      sourceFileName: path_.relative(process.cwd(), data.fileName.replace(/\\/g, '/')),
    })
    babelOpts.plugins = babelOpts.plugins.concat([
      fableUtils.babelPlugins.getRemoveUnneededNulls(),
      fableUtils.babelPlugins.getTransformMacroExpressions(babel.template),
    ])

    const { code } = babel.transformFromAst(data, fs.readFileSync(path, 'utf8'), babelOpts)

    return { ...logs, code, success: true }
  }
}

parse(path_.join(__dirname, 'src/FableDemo.fsproj'), true)
parse(path_.join(__dirname, 'src/FableDemo.fs')).then((result) =>
  console.log('RESULT:', JSON.stringify(result)),
)
