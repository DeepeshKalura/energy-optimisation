import geocoder

def location_with_ip_address() -> tuple[str, list[float]]:
  """
  Retrieves the location and latitude/longitude coordinates based on the IP address of the user.

  Returns:
    A tuple containing the location (address) and latitude/longitude coordinates.

  Example:
    >>> location_with_ip_address()
    ('New York, NY, USA', [40.7128, -74.0060])
  """
  g = geocoder.ip('me')
  latlan = g.latlng
  location = g.address
  return (location, latlan) 


