# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository. Update this file whenever anything about the project changes significantly.

## Commands

### Development
- `yarn` - Install dependencies
- `yarn dev` - Start Next.js development server at http://localhost:3000
- `yarn build` - Build for production (runs prebuild.sh, Next build, postbuild.sh)
- `yarn start` - Start production server

### Update Scripts
- `./update_coins.sh` - Update coins configuration and seed nodes
- `./update_wasm.sh $zipfile_url` - Update WASM binary from URL
- `./update_coins_url.sh $github_raw_url` - Update coins file from GitHub

## Architecture Overview

### Tech Stack
- **Framework**: Next.js 13.5.4 configured as SPA with static export
- **State Management**: Recoil with modular store pattern
- **Styling**: Tailwind CSS with custom color scheme
- **WASM Integration**: Komodo DeFi Framework (KDF) WebAssembly module

### Project Structure
```
/app/                 # Next.js app router
  layout.jsx         # Root layout
  page.jsx          # Main page with RecoilRoot
/src/
  App.jsx           # Core application component
  /components/      # React components
    Mm2Panel.jsx    # MM2 service management (WASM integration point)
    RpcPanel.jsx    # RPC interface
    RpcResponsePanel.jsx
    Mm2LogsPanel.jsx
  /store/           # Recoil state modules
    atomKeys.js     # Centralized atom keys
    /mm2/, /rpc/, /modals/, etc.
  /shared-functions/  # Utility functions
/coins/             # Cryptocurrency configurations
/methods/           # RPC method definitions (Postman collections)
/public/
  kdflib_bg.wasm    # WASM binary
```

### State Management Pattern
Each store module exports a custom hook (e.g., `useMm2PanelState()`) that provides state and setters. All atom keys are centralized in `atomKeys.js`.

### WASM Integration
The KDF WASM module is loaded in `Mm2Panel.jsx` and provides:
- `mm2_main()` - Start MM2 service
- `mm2_stop()` - Stop MM2 service
- `mm2_main_status()` - Get status
- `mm2_version()` - Get version

### Panel Layout System
The app uses resizable panels with draggable dividers:
- Sidebar (40px default)
- Main area split between MM2 and RPC panels
- Bottom panel for logs/responses (220px default)

### Build Process
1. `prebuild.sh` - Renames WASM with version
2. Next.js build - Creates static export in `/dist/`
3. `postbuild.sh` - Restores WASM filename

### Key Files to Understand
- `src/components/Mm2Panel.jsx` - WASM loading and MM2 service management
- `src/shared-functions/rpcRequest.js` - RPC request handling
- `src/store/atomKeys.js` - All Recoil atom keys
- `next.config.mjs` - Next.js configuration (static export)

## Tailwind CSS Rules and Best Practices

### Core Principles

- **Always use Tailwind CSS v4.1+** - Ensure the codebase is using the latest version
- **Do not use deprecated or removed utilities** - ALWAYS use the replacement
- **Never use `@apply`** - Use CSS variables, the `--spacing()` function, or framework components instead
- **Check for redundant classes** - Remove any classes that aren't necessary
- **Group elements logically** to simplify responsive tweaks later

### Upgrading to Tailwind CSS v4

#### Before Upgrading

- **Always read the upgrade documentation first** - Read https://tailwindcss.com/docs/upgrade-guide and https://tailwindcss.com/blog/tailwindcss-v4 before starting an upgrade.
- Ensure the git repository is in a clean state before starting

#### Upgrade Process

1. Run the upgrade command: `npx @tailwindcss/upgrade@latest` for both major and minor updates
2. The tool will convert JavaScript config files to the new CSS format
3. Review all changes extensively to clean up any false positives
4. Test thoroughly across your application

### Breaking Changes Reference

#### Removed Utilities (NEVER use these in v4)

| ❌ Deprecated           | ✅ Replacement                                    |
| ----------------------- | ------------------------------------------------- |
| `bg-opacity-*`          | Use opacity modifiers like `bg-black/50`          |
| `text-opacity-*`        | Use opacity modifiers like `text-black/50`        |
| `border-opacity-*`      | Use opacity modifiers like `border-black/50`      |
| `divide-opacity-*`      | Use opacity modifiers like `divide-black/50`      |
| `ring-opacity-*`        | Use opacity modifiers like `ring-black/50`        |
| `placeholder-opacity-*` | Use opacity modifiers like `placeholder-black/50` |
| `flex-shrink-*`         | `shrink-*`                                        |
| `flex-grow-*`           | `grow-*`                                          |
| `overflow-ellipsis`     | `text-ellipsis`                                   |
| `decoration-slice`      | `box-decoration-slice`                            |
| `decoration-clone`      | `box-decoration-clone`                            |

#### Renamed Utilities (ALWAYS use the v4 name)

| ❌ v3              | ✅ v4              |
| ------------------ | ------------------ |
| `bg-gradient-*`    | `bg-linear-*`      |
| `shadow-sm`        | `shadow-xs`        |
| `shadow`           | `shadow-sm`        |
| `drop-shadow-sm`   | `drop-shadow-xs`   |
| `drop-shadow`      | `drop-shadow-sm`   |
| `blur-sm`          | `blur-xs`          |
| `blur`             | `blur-sm`          |
| `backdrop-blur-sm` | `backdrop-blur-xs` |
| `backdrop-blur`    | `backdrop-blur-sm` |
| `rounded-sm`       | `rounded-xs`       |
| `rounded`          | `rounded-sm`       |
| `outline-none`     | `outline-hidden`   |
| `ring`             | `ring-3`           |

### Layout and Spacing Rules

#### Flexbox and Grid Spacing

##### Always use gap utilities for internal spacing

Gap provides consistent spacing without edge cases (no extra space on last items). It's cleaner and more maintainable than margins on children.

```html
<!-- ❌ Don't do this -->
<div class="flex">
  <div class="mr-4">Item 1</div>
  <div class="mr-4">Item 2</div>
  <div>Item 3</div>
  <!-- No margin on last -->
</div>

<!-- ✅ Do this instead -->
<div class="flex gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

##### Gap vs Space utilities

- **Never use `space-x-*` or `space-y-*` in flex/grid layouts** - always use gap
- Space utilities add margins to children and have issues with wrapped items
- Gap works correctly with flex-wrap and all flex directions

```html
<!-- ❌ Avoid space utilities in flex containers -->
<div class="flex flex-wrap space-x-4">
  <!-- Space utilities break with wrapped items -->
</div>

<!-- ✅ Use gap for consistent spacing -->
<div class="flex flex-wrap gap-4">
  <!-- Gap works perfectly with wrapping -->
</div>
```

#### General Spacing Guidelines

- **Prefer top and left margins** over bottom and right margins (unless conditionally rendered)
- **Use padding on parent containers** instead of bottom margins on the last child
- **Always use `min-h-dvh` instead of `min-h-screen`** - `min-h-screen` is buggy on mobile Safari
- **Prefer `size-*` utilities** over separate `w-*` and `h-*` when setting equal dimensions
- For max-widths, prefer the container scale (e.g., `max-w-2xs` over `max-w-72`)

### Typography Rules

#### Line Heights

- **Never use `leading-*` classes** - Always use line height modifiers with text size
- **Always use fixed line heights from the spacing scale** - Don't use named values

```html
<!-- ❌ Don't do this -->
<p class="text-base leading-7">Text with separate line height</p>
<p class="text-lg leading-relaxed">Text with named line height</p>

<!-- ✅ Do this instead -->
<p class="text-base/7">Text with line height modifier</p>
<p class="text-lg/8">Text with specific line height</p>
```

#### Font Size Reference

Be precise with font sizes - know the actual pixel values:

- `text-xs` = 12px
- `text-sm` = 14px
- `text-base` = 16px
- `text-lg` = 18px
- `text-xl` = 20px

### Color and Opacity

#### Opacity Modifiers

**Never use `bg-opacity-*`, `text-opacity-*`, etc.** - use the opacity modifier syntax:

```html
<!-- ❌ Don't do this -->
<div class="bg-red-500 bg-opacity-60">Old opacity syntax</div>

<!-- ✅ Do this instead -->
<div class="bg-red-500/60">Modern opacity syntax</div>
```

### Responsive Design

#### Breakpoint Optimization

- **Check for redundant classes across breakpoints**
- **Only add breakpoint variants when values change**

```html
<!-- ❌ Redundant breakpoint classes -->
<div class="px-4 md:px-4 lg:px-4">
  <!-- md:px-4 and lg:px-4 are redundant -->
</div>

<!-- ✅ Efficient breakpoint usage -->
<div class="px-4 lg:px-8">
  <!-- Only specify when value changes -->
</div>
```

### Dark Mode

#### Dark Mode Best Practices

- Use the plain `dark:` variant pattern
- Put light mode styles first, then dark mode styles
- Ensure `dark:` variant comes before other variants

```html
<!-- ✅ Correct dark mode pattern -->
<div class="bg-white text-black dark:bg-black dark:text-white">
  <button class="hover:bg-gray-100 dark:hover:bg-gray-800">Click me</button>
</div>
```

### Gradient Utilities

- **ALWAYS Use `bg-linear-*` instead of `bg-gradient-*` utilities** - The gradient utilities were renamed in v4
- Use the new `bg-radial` or `bg-radial-[<position>]` to create radial gradients
- Use the new `bg-conic` or `bg-conic-*` to create conic gradients

```html
<!-- ✅ Use the new gradient utilities -->
<div class="h-14 bg-linear-to-br from-violet-500 to-fuchsia-500"></div>
<div
  class="size-18 bg-radial-[at_50%_75%] from-sky-200 via-blue-400 to-indigo-900 to-90%"
></div>
<div
  class="size-24 bg-conic-180 from-indigo-600 via-indigo-50 to-indigo-600"
></div>

<!-- ❌ Do not use bg-gradient-* utilities -->
<div class="h-14 bg-gradient-to-br from-violet-500 to-fuchsia-500"></div>
```

### Working with CSS Variables

#### Accessing Theme Values

Tailwind CSS v4 exposes all theme values as CSS variables:

```css
/* Access colors, and other theme values */
.custom-element {
  background: var(--color-red-500);
  border-radius: var(--radius-lg);
}
```

#### The `--spacing()` Function

Use the dedicated `--spacing()` function for spacing calculations:

```css
.custom-class {
  margin-top: calc(100vh - --spacing(16));
}
```

#### Extending theme values

Use CSS to extend theme values:

```css
@import "tailwindcss";

@theme {
  --color-mint-500: oklch(0.72 0.11 178);
}
```

```html
<div class="bg-mint-500">
  <!-- ... -->
</div>
```

### New v4 Features

#### Container Queries

Use the `@container` class and size variants:

```html
<article class="@container">
  <div class="flex flex-col @md:flex-row @lg:gap-8">
    <img class="w-full @md:w-48" />
    <div class="mt-4 @md:mt-0">
      <!-- Content adapts to container size -->
    </div>
  </div>
</article>
```

#### Container Query Units

Use container-based units like `cqw` for responsive sizing:

```html
<div class="@container">
  <h1 class="text-[50cqw]">Responsive to container width</h1>
</div>
```

#### Text Shadows (v4.1)

Use text-shadow-\* utilities from text-shadow-2xs to text-shadow-lg:

```html
<!-- ✅ Text shadow examples -->
<h1 class="text-shadow-lg">Large shadow</h1>
<p class="text-shadow-sm/50">Small shadow with opacity</p>
```

#### Masking (v4.1)

Use the new composable mask utilities for image and gradient masks:

```html
<!-- ✅ Linear gradient masks on specific sides -->
<div class="mask-t-from-50%">Top fade</div>
<div class="mask-b-from-20% mask-b-to-80%">Bottom gradient</div>
<div class="mask-linear-from-white mask-linear-to-black/60">
  Fade from white to black
</div>

<!-- ✅ Radial gradient masks -->
<div class="mask-radial-[100%_100%] mask-radial-from-75% mask-radial-at-left">
  Radial mask
</div>
```

### Component Patterns

#### Avoiding Utility Inheritance

Don't add utilities to parents that you override in children:

```html
<!-- ❌ Avoid this pattern -->
<div class="text-center">
  <h1>Centered Heading</h1>
  <div class="text-left">Left-aligned content</div>
</div>

<!-- ✅ Better approach -->
<div>
  <h1 class="text-center">Centered Heading</h1>
  <div>Left-aligned content</div>
</div>
```

#### Component Extraction

- Extract repeated patterns into framework components, not CSS classes
- Keep utility classes in templates/JSX
- Use data attributes for complex state-based styling

### CSS Best Practices

#### Nesting Guidelines

- Use nesting when styling both parent and children
- Avoid empty parent selectors

```css
/* ✅ Good nesting - parent has styles */
.card {
  padding: --spacing(4);

  > .card-title {
    font-weight: bold;
  }
}

/* ❌ Avoid empty parents */
ul {
  > li {
    /* Parent has no styles */
  }
}
```

### Common Pitfalls to Avoid

1. **Using old opacity utilities** - Always use `/opacity` syntax like `bg-red-500/60`
2. **Redundant breakpoint classes** - Only specify changes
3. **Space utilities in flex/grid** - Always use gap
4. **Leading utilities** - Use line-height modifiers like `text-sm/6`
5. **Arbitrary values** - Use the design scale
6. **@apply directive** - Use components or CSS variables
7. **min-h-screen on mobile** - Use min-h-dvh
8. **Separate width/height** - Use size utilities when equal
9. **Arbitrary values** - Always use Tailwind's predefined scale whenever possible (e.g., use `ml-4` over `ml-[16px]`)