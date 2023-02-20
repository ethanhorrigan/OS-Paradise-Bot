'''Nickname handler unit tests'''
# pylint: disable=wrong-import-position
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), \
    '../../../')))
import pytest
from unittest.mock import AsyncMock, patch
from src.handlers.nickname_handler import update_member_nickname, process_nickname_query
import src.osp_logger as log
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), \
    '../../../', 'src')))

member = AsyncMock()
timestamp = log.get_timestamp()

@pytest.mark.asyncio
@patch('builtins.print')
async def test_update_member_nickname(mock_print):
    member.nick = 'old_nickname'
    nickname_query = 'Test Nickname'
    mock_message = f'Updating nickname for {member.nick} to {nickname_query}'
    await update_member_nickname(member, nickname_query)
    member.edit.assert_called_once_with(nick=nickname_query)
    mock_print.assert_called_once_with(f'[{timestamp}] INFO: {mock_message}')

@pytest.mark.asyncio
@patch('handlers.nickname_handler.wom_lookup_user')
async def test_process_nickname_query(mock_wom_lookup_user):

    users, valid_users, invalid_users = await \
        process_nickname_query('Alice|Charlie|Bob')
    assert users == ['Alice', 'Charlie', 'Bob']
    assert valid_users == ['Alice', 'Charlie', 'Bob']
    assert invalid_users == []

    users, valid_users, invalid_users = await \
        process_nickname_query('testuser123456789')
    assert users == ['testuser123456789']
    assert valid_users == []
    assert invalid_users == ['testuser123456789']

    users, valid_users, invalid_users = await \
        process_nickname_query('Alice|testuser123456789')
    assert users == ['Alice', 'testuser123456789']
    assert valid_users == ['Alice']
    assert invalid_users == ['testuser123456789']
