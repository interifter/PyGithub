############################ Copyrights and license ############################
#                                                                              #
# Copyright 2020 Florent Clarret <florent.clarret@gmail.com>                   #
# Copyright 2020 Steve Kowalik <steven@wedontsleep.org>                        #
# Copyright 2023 Enrico Minack <github@enrico.minack.dev>                      #
# Copyright 2023 Jirka Borovec <6035284+Borda@users.noreply.github.com>        #
# Copyright 2025 Enrico Minack <github@enrico.minack.dev>                      #
#                                                                              #
# This file is part of PyGithub.                                               #
# http://pygithub.readthedocs.io/                                              #
#                                                                              #
# PyGithub is free software: you can redistribute it and/or modify it under    #
# the terms of the GNU Lesser General Public License as published by the Free  #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# PyGithub is distributed in the hope that it will be useful, but WITHOUT ANY  #
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS    #
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more #
# details.                                                                     #
#                                                                              #
# You should have received a copy of the GNU Lesser General Public License     #
# along with PyGithub. If not, see <http://www.gnu.org/licenses/>.             #
#                                                                              #
################################################################################

from __future__ import annotations

from datetime import datetime, timezone

from . import Framework


class ProjectColumn(Framework.TestCase):
    def setUp(self):
        super().setUp()
        self.get_project_column = self.g.get_project_column(8700460)
        self.move_project_column = self.g.get_project_column(8748065)
        proj = self.g.get_project(1682941)
        self.col = proj.get_columns()[0]

    # See https://developer.github.com/v3/projects/columns/#get-a-project-column
    def testAttributes(self):
        col = self.col
        self.assertEqual(col.cards_url, "https://api.github.com/projects/columns/3138830/cards")
        self.assertEqual(col.created_at.year, 2018)
        self.assertEqual(col.id, 3138830)
        self.assertEqual(col.name, "To Do")
        self.assertEqual(col.node_id, "MDEzOlByb2plY3RDb2x1bW4zMTM4ODMw")
        self.assertEqual(col.project_url, "https://api.github.com/projects/1682941")
        self.assertEqual(col.updated_at, datetime(2018, 8, 1, 4, 7, 35, tzinfo=timezone.utc))
        self.assertEqual(col.url, "https://api.github.com/projects/columns/3138830")
        self.assertEqual(repr(col), 'ProjectColumn(name="To Do")')

    def testCreate(self):
        repo = self.g.get_user().get_repo("PyGithub")
        project = repo.create_project("Project created by PyGithub", "Project Body")
        column = project.create_column(
            "Project Column created by PyGithub",
        )
        self.assertEqual(column.id, 3999333)

    def testGetProjectColumn(self):
        self.assertEqual(self.get_project_column.id, 8700460)
        self.assertEqual(self.get_project_column.name, "c1")
        self.assertEqual(
            self.get_project_column.cards_url,
            "https://api.github.com/projects/columns/8700460/cards",
        )
        self.assertEqual(self.get_project_column.node_id, "MDEzOlByb2plY3RDb2x1bW44NzAwNDYw")
        self.assertEqual(
            self.get_project_column.project_url,
            "https://api.github.com/projects/4294766",
        )
        self.assertEqual(
            self.get_project_column.url,
            "https://api.github.com/projects/columns/8700460",
        )
        self.assertEqual(
            self.get_project_column.created_at,
            datetime(2020, 4, 13, 20, 29, 53, tzinfo=timezone.utc),
        )
        self.assertEqual(
            self.get_project_column.updated_at,
            datetime(2020, 4, 14, 18, 9, 38, tzinfo=timezone.utc),
        )

    def testGetAllCards(self):
        cards = self.get_project_column.get_cards(archived_state="all")
        self.assertEqual(cards.totalCount, 3)
        self.assertEqual(cards[0].id, 36285184)
        self.assertEqual(cards[0].note, "Note3")
        self.assertEqual(cards[1].id, 36281526)
        self.assertEqual(cards[1].note, "Note2")
        self.assertEqual(cards[2].id, 36281516)
        self.assertEqual(cards[2].note, "Note1")

    def testGetArchivedCards(self):
        cards = self.get_project_column.get_cards(archived_state="archived")
        self.assertEqual(cards.totalCount, 1)
        self.assertEqual(cards[0].id, 36281516)
        self.assertEqual(cards[0].note, "Note1")

    def testGetNotArchivedCards(self):
        cards = self.get_project_column.get_cards(archived_state="not_archived")
        self.assertEqual(cards.totalCount, 2)
        self.assertEqual(cards[0].id, 36285184)
        self.assertEqual(cards[0].note, "Note3")
        self.assertEqual(cards[1].id, 36281526)
        self.assertEqual(cards[1].note, "Note2")

    def testGetCards(self):
        cards = self.get_project_column.get_cards()
        self.assertEqual(cards.totalCount, 2)
        self.assertEqual(cards[0].id, 36285184)
        self.assertEqual(cards[0].note, "Note3")
        self.assertEqual(cards[1].id, 36281526)
        self.assertEqual(cards[1].note, "Note2")

    def testCreateCard(self):
        new_card = self.get_project_column.create_card(note="NewCard")
        self.assertEqual(new_card.id, 36290228)
        self.assertEqual(new_card.note, "NewCard")

    def testDelete(self):
        project_column = self.g.get_project_column(8747987)
        self.assertTrue(project_column.delete())

    def testEdit(self):
        self.move_project_column.edit("newTestColumn")
        self.assertEqual(self.move_project_column.id, 8748065)
        self.assertEqual(self.move_project_column.name, "newTestColumn")

    def testMoveFirst(self):
        self.assertTrue(self.move_project_column.move(position="first"))

    def testMoveLast(self):
        self.assertTrue(self.move_project_column.move(position="last"))

    def testMoveAfter(self):
        self.assertTrue(self.move_project_column.move(position="after:8700460"))
