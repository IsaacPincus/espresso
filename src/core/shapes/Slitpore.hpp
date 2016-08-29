/*
  Copyright (C) 2010,2011,2012,2013,2014 The ESPResSo project
  Copyright (C) 2002,2003,2004,2005,2006,2007,2008,2009,2010
  Max-Planck-Institute for Polymer Research, Theory Group

  This file is part of ESPResSo.

  ESPResSo is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  ESPResSo is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef __SLITPORE_HPP
#define __SLITPORE_HPP

#include "Shape.hpp"

namespace Shapes {
class Slitpore : public Shape {
public:
  Slitpore() : m_pore_mouth(0.0), m_upper_smoothing_radius(0.0), m_lower_smoothing_radius(0.0), 
	           m_channel_width(0.0), m_pore_width(0.0), m_pore_length(0.0) {}

  int calculate_dist(const double *ppos, double *dist, double *vec) const override;

  double const &pore_mouth() const { return m_pore_mouth; }
  double const &upper_smoothing_radius() const { return m_upper_smoothing_radius; }
  double const &lower_smoothing_radius() const { return m_lower_smoothing_radius; }
  double const &channel_width() const { return m_channel_width; }
  double const &pore_width() const { return m_pore_width; }
  double const &pore_length() const { return m_pore_length; }
private:
  double m_pore_mouth;
  double m_upper_smoothing_radius;
  double m_lower_smoothing_radius;
  double m_channel_width;
  double m_pore_width;
  double m_pore_length;
};
};

#endif
