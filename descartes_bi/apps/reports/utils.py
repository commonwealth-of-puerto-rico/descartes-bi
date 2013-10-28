from __future__ import absolute_import

#
#    Copyright (C) 2013  Roberto Rosario
#    This file is part of descartes-bi.
#
#    descartes-bi is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    descartes-bi is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with descartes-bi.  If not, see <http://www.gnu.org/licenses/>.
#
from django.contrib.auth.models import User

from .models import Report, Menuitem, GroupPermission, UserPermission


def get_allowed_object_for_user(user):
    reports_allowed = []
    menuitems_allowed = []
    try:
        user = User.objects.get(username=user)

        #staff gets all reports & menuitems
        if user.is_staff:
            return {
                'reports': Report.objects.all(),
                'menuitems': Menuitem.objects.all()
            }

        for group in user.groups.all():
            try:
                gp = GroupPermission.objects.get(group=group)
                for report in gp.reports.all():
                    if report not in reports_allowed:
                        reports_allowed.append(report)

            except:
                #Group does have permissions
                pass
        try:
            up = UserPermission.objects.get(user=user)
            if up.union == 'O':  # Overwrite
                reports_allowed = []

            if up.union == 'I' or up.union == 'O':  # Inclusive
                for report in up.reports.all():
                    if report not in reports_allowed:
                        reports_allowed.append(report)
            elif up.union == 'E':  # Exclusive
                for report in up.reports.all():
                    if report in reports_allowed:
                        reports_allowed.remove(report)

        except:
            #Not User permission for this user
            pass
    except:
        #unkown user or anonymous
        pass

    for report in reports_allowed:
        menuitems = report.menuitem_set.all()
        for menuitem in menuitems:
            if menuitem not in menuitems_allowed:
                menuitems_allowed.append(menuitem)

    return {
        'reports': reports_allowed,
        'menuitems': menuitems_allowed
    }
