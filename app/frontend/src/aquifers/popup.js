import mapboxgl from 'mapbox-gl'

import { getLngLatOfPointFeature } from '../common/mapbox/geometry'
import {
  toggleAquiferHover,
  WELLS_BASE_AND_ARTESIAN_LAYER_ID,
  AQUIFERS_FILL_LAYER_ID,
  WELLS_EMS_LAYER_ID,
  WELLS_UNCORRELATED_LAYER_ID
} from '../common/mapbox/layers'

// Creates a <div> for the well's popup content
export function createWellPopupElement ($router, wellFeatureProperties, options = {}) {
  const {
    well_tag_number: wellTagNumber,
    identification_plate_number: identificationPlateNumber,
    street_address: streetAddress,
    aquifer_id: aquiferId,
    ems
  } = wellFeatureProperties

  const routes = {
    wellDetail: { name: 'wells-detail', params: { id: wellTagNumber } },
    aquiferDetail: { name: 'aquifers-view', params: { id: aquiferId } }
  }

  let correlatedAquiferItem = 'Uncorrelated well'
  if (aquiferId) {
    // well is correlated to diff aquifer = link it
    const aquiferDetailsUrl = $router.resolve(routes.aquiferDetail)
    correlatedAquiferItem = `Correlated to <a href="${aquiferDetailsUrl.href}" data-route-name="aquiferDetail">aquifer ${aquiferId}</a>`

    // If there is an optional `currentAquiferId` check to see if this well's aquifer_id is the same
    // as `currentAquiferId`. If it is then don't bother linking to the aquifer.
    if (options.currentAquiferId !== undefined && aquiferId === options.currentAquiferId) {
      correlatedAquiferItem = `Correlated to aquifer ${aquiferId}`
    }
  }

  const url = $router.resolve(routes.wellDetail)

  const items = [
    `Well Tag Number: <a href="${url.href}" data-route-name="wellDetail">${wellTagNumber}</a>`,
    `Identification Plate Number: ${identificationPlateNumber || '—'}`,
    `Address: ${streetAddress || '—'}`,
    correlatedAquiferItem,
    ems ? `EMS ID: ${ems}` : null
  ]

  const container = document.createElement('div')
  container.className = 'leaflet-popup-aquifer'
  container.innerHTML = items.filter(Boolean).join('<br>')
  // Add onclick handlers for every anchor
  const anchors = container.querySelectorAll('a')
  for (let i = 0; i < anchors.length; i++) {
    anchors[i].onclick = (e) => {
      if (!e.ctrlKey) {
        e.preventDefault()
        const routeName = anchors[i].getAttribute('data-route-name')
        $router.push(routes[routeName])
      }
    }
  }
  return container
}

// Creates a <div> for the aquifer's popup content
export function createAquiferPopupElement (map, $router, point) {
  const container = document.createElement('div')
  container.className = 'mapbox-popup-aquifer'
  const ul = document.createElement('ul')
  ul.className = 'm-0 p-0'
  ul.style = 'list-style: none'
  container.appendChild(ul)

  var features = map.queryRenderedFeatures(point, { layers: [ 'aquifer-fill' ] })
  features.forEach((feature) => {
    const { aquifer_id: aquiferId } = feature.properties
    const route = { name: 'aquifers-view', params: { id: aquiferId } }
    const url = $router.resolve(route)
    const li = document.createElement('li')
    li.className = 'm-0 p-0'
    li.innerHTML = `<a href="${url.href}">Aquifer ${aquiferId}</a>`
    const a = li.querySelector('a')
    a.onclick = (e) => {
      if (!e.ctrlKey) {
        e.preventDefault()
        $router.push(route)
      }
    }
    // highlight this aquifer on mouseover of the aquifer ID in the popup
    li.onmouseenter = () => {
      toggleAquiferHover(map, aquiferId, true)
    }
    li.onmouseleave = () => {
      toggleAquiferHover(map, aquiferId, false)
    }
    ul.appendChild(li)
  })
  return container
}

// The tooltip is currently shows exactly the same data as the popup but they could be different
export function createWellTooltipElement ($router, wellFeatureProperties, options) {
  return createWellPopupElement($router, wellFeatureProperties, options)
}

// The tooltip is currently shows exactly the same data as the popup but they could be different
export function createAquiferTooltipElement (map, $router, point) {
  return createAquiferPopupElement(map, $router, point)
}

const DEFAULT_WELL_LAYER_IDS = [
  WELLS_BASE_AND_ARTESIAN_LAYER_ID,
  WELLS_EMS_LAYER_ID,
  WELLS_UNCORRELATED_LAYER_ID
]

// Adds mouse event listeners to the map which will show the tooltip for an aquifer or well
export function setupMapTooltips (map, $router, options = {}) {
  const wellsTooltip = new mapboxgl.Popup()
  const aquifersTooltip = new mapboxgl.Popup()

  const aquiferFillLayerId = options.aquiferFillLayerId || AQUIFERS_FILL_LAYER_ID
  const wellsLayerIds = options.wellsLayerIds || DEFAULT_WELL_LAYER_IDS

  let overAquifer = false
  wellsLayerIds.forEach((wellLayerId) => {
    map.on('mousemove', wellLayerId, (e) => {
      map.getCanvas().style.cursor = 'pointer'

      aquifersTooltip.remove()

      if (map.popup.isOpen()) { return }

      const feature = e.features[0]
      const contentDiv = createWellPopupElement($router, feature.properties, options)
      wellsTooltip
        .setLngLat(getLngLatOfPointFeature(feature))
        .setDOMContent(contentDiv)
        .addTo(map)
    })

    map.on('mouseleave', wellLayerId, () => {
      map.getCanvas().style.cursor = ''
      wellsTooltip.remove()
      if (overAquifer && !map.popup.isOpen()) {
        aquifersTooltip.addTo(map)
      }
    })
  })

  map.on('mouseenter', aquiferFillLayerId, (e) => {
    overAquifer = true
    if (map.popup.isOpen() || wellsTooltip.isOpen()) { return }

    const contentDiv = createAquiferTooltipElement(map, $router, e.point)
    aquifersTooltip
      .setDOMContent(contentDiv)
      .setLngLat(e.lngLat)
      .addTo(map)
  })

  map.on('mousemove', aquiferFillLayerId, (e) => {
    if (map.popup.isOpen() || wellsTooltip.isOpen()) { return }

    const contentDiv = createAquiferTooltipElement(map, $router, e.point)
    aquifersTooltip
      .setDOMContent(contentDiv)
      .setLngLat(e.lngLat)
      .addTo(map)
  })

  map.on('mouseleave', aquiferFillLayerId, () => {
    aquifersTooltip.remove()
    overAquifer = false
  })
}

// Adds mouse event listeners to the map which will show the popup for the clicked well or aquifer
export function setupMapPopups (map, $router, options = {}) {
  const wellsLayerIds = options.wellsLayerIds || DEFAULT_WELL_LAYER_IDS
  const aquiferFillLayerId = options.aquiferFillLayerId || AQUIFERS_FILL_LAYER_ID

  let clickedOnWell = false
  const popup = new mapboxgl.Popup()
  popup.on('close', () => {
    clickedOnWell = false
  })
  map.popup = popup

  wellsLayerIds.forEach((wellLayerId) => {
    map.on('click', wellLayerId, (e) => {
      // Check to see if we have already clicked on a well (could be an invisible EMS layer click)
      if (clickedOnWell) { return }
      clickedOnWell = true
      const feature = e.features[0]
      const contentDiv = createWellPopupElement($router, feature.properties, options)
      popup
        .setLngLat(getLngLatOfPointFeature(feature))
        .setDOMContent(contentDiv)
        .addTo(map)
    })
  })

  map.on('click', aquiferFillLayerId, (e) => {
    if (clickedOnWell) { return }
    if (map.hoveredAquiferId) {
      toggleAquiferHover(map, map.hoveredAquiferId, false)
    }

    const contentDiv = createAquiferPopupElement(map, $router, e.point)
    popup
      .setLngLat(e.lngLat)
      .setDOMContent(contentDiv)
      .addTo(map)
  })
}