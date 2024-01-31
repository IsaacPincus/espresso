/*
 * Copyright (C) 2010-2019 The ESPResSo project
 *
 * This file is part of ESPResSo.
 *
 * ESPResSo is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * ESPResSo is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
#include "PidObservable.hpp"

#include "partCfg_global.hpp"

#include <boost/range/algorithm/transform.hpp>

namespace Observables {
std::vector<double> PidObservable::operator()() const {
  std::vector<const Particle *> particles(ids().size());

  boost::transform(ids(), particles.begin(),
                   [](int id) { return &partCfg()[id]; });

  return this->evaluate(particles);
}
} // namespace Observables